from fastapi import APIRouter

from piplant.sensors.raspberry import raspberry_sensor as sensor

router = APIRouter(tags=['raspberry'])


@router.get('/raspberry/cpu')
async def get_cpu():
    return await sensor.get_cpu_data()

@router.get('/raspberry/disk')
async def get_disk():
    return await sensor.get_disk_data()