import time

from dht11 import DHT11

from piplant import settings

from pydantic import BaseModel


class AmbientData(BaseModel):
    time = 0
    temperature = 0.0
    humidity = 0.0


class DHT11Sensor:

    def __init__(self):
        self.dht11 = DHT11(pin=settings.DHT11_PIN)
        self.data = AmbientData()

    async def get_data(self):
        unix_time = int(time.time())
        if (unix_time - self.data.time) > 5:
            data = self.dht11.read()
            if data.is_valid():
                self.data.time = unix_time
                self.data.temperature = data.temperature
                self.data.humidity = data.humidity

        return self.data


dht11_sensor = DHT11Sensor()
