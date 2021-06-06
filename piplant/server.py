import sys

import RPi.GPIO as GPIO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from piplant.sensors import ambient, camera, raspberry, relays
from piplant.settings import settings
from piplant.database import pool


app = FastAPI(
    title="Piplant",
    description="IOT project that lets you control and monitor plants remotely",
    version="0.1.0"
)
app.include_router(ambient.router)
app.include_router(camera.router)
app.include_router(raspberry.router)
app.include_router(relays.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

@app.on_event('startup')
async def startup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    try:
        await pool.start(host=settings.database.host, port=settings.database.port, database=settings.database.name,
                         user=settings.database.username, password=settings.database.password)
    except Exception as ex:
        sys.exit(1)

    async with pool.pool.acquire() as connection:
        async with connection.transaction():
            async for relay in connection.cursor('SELECT pin, active_low FROM relays'):
                await relays.toggle_pin(relay['pin'], relay['active_low'], False)
