import aiofiles
import os
import re
import time

from pydantic import BaseModel


class CpuData(BaseModel):
    time = 0
    temperature = 0.0
    load = 0.0


class MemoryData(BaseModel):
    time = 0
    size = 0.0
    used = 0.0
    free = 0.0


class RaspberrySensor:

    def __init__(self):
        self.cpu_data = CpuData()
        self.disk_data = MemoryData()

    async def get_cpu_data(self):
        unix_time = int(time.time())
        if (unix_time - self.cpu_data.time) > 5:
            self.cpu_data.time = unix_time
            async with aiofiles.open('/sys/class/thermal/thermal_zone0/temp') as f:
                self.cpu_data.temperature = float(await f.read()) / 1000

            async with aiofiles.open('/proc/loadavg') as f:
                data = await f.read()
                self.cpu_data.load = float(re.search(r'(\d+.?\d+)', data).group())

        return self.cpu_data

    async def get_disk_data(self):
        unix_time = int(time.time())
        if (unix_time - self.disk_data.time) > 5:
            data = os.statvfs('/')
            self.disk_data.time = unix_time
            self.disk_data.size = data.f_bsize * data.f_blocks / 1024000000
            self.disk_data.free = data.f_bsize * data.f_bavail / 1024000000
            self.disk_data.used = self.disk_data.size - self.disk_data.free

        return self.disk_data


raspberry_sensor = RaspberrySensor()
