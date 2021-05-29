from fastapi import FastAPI

from piplant.sensors import ambient, raspberry

import RPi.GPIO as GPIO

app = FastAPI()
app.include_router(ambient.router)
app.include_router(raspberry.router)


@app.on_event('startup')
def startup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
