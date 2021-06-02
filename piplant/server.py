import logging
import sys

import asyncpg
import RPi.GPIO as GPIO

from fastapi import FastAPI

from piplant.sensors import ambient, camera, raspberry
from piplant.settings import settings


class ConnectionPool:

    def __init__(self):
        self.pool = None

    async def start(self, **kwargs):
        self.pool = await asyncpg.create_pool(**kwargs)


pool = ConnectionPool()

app = FastAPI()
app.include_router(ambient.router)
app.include_router(camera.router)
app.include_router(raspberry.router)


@app.on_event('startup')
async def startup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    for relay in settings.relays:
        GPIO.setup(relay.pin, GPIO.OUT, initial=GPIO.HIGH)

    try:
        await pool.start(host=settings.database.host, port=settings.database.port, database=settings.database.name,
                         user=settings.database.username, password=settings.database.password)
    except Exception as ex:
        sys.exit(1)
