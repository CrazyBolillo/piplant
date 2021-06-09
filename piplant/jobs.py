import asyncio

from piplant.database import pool
from piplant.sensors.ambient import sensor as ambient_sensor


async def measure_ambient():
    temperature = 0
    humidity = 0
    count = 0
    time = 0

    for i in range(5):
        data = await ambient_sensor.get_data()
        if time != data.time:
            time = data.time
            temperature += data.temperature
            humidity += data.humidity
            count += 1
        await asyncio.sleep(6)

    if count != 0:
        temperature /= count
        humidity /= count
        async with pool.pool.acquire() as connection:
            stmt = await connection.prepare('INSERT INTO ambient_measures (temperature, humidity) VALUES ($1, $2)')
            await stmt.fetchval(temperature, humidity)



