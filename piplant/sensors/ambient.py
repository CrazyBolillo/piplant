import time

from fastapi import APIRouter
from dht11 import DHT11
from pydantic import BaseModel

from piplant.settings import settings


class AmbientData(BaseModel):
    time = 0
    temperature = 0.0
    humidity = 0.0


class DHT11Sensor:

    def __init__(self):
        self.dht11 = DHT11(pin=settings.dht11_pin)
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


sensor = DHT11Sensor()

router = APIRouter(tags=['ambient'])


@router.get('/ambient', response_model=AmbientData)
async def get():
    """
    Measures the relative humidity and temperature.
    :return: A measurement of relative humidity and temperature. Measurement is guaranteed to be 5 seconds old or less.
    (UNIX time)
    """
    return await sensor.get_data()

