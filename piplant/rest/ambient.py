from fastapi import APIRouter

from piplant.sensors.dht11 import dht11_sensor as sensor

router = APIRouter(tags=['ambient'])


@router.get('/ambient')
async def get():
    return await sensor.get_cpu_data()
