import RPi.GPIO as GPIO

from fastapi import FastAPI

from piplant.sensors import ambient, camera, raspberry
from piplant.settings import settings

app = FastAPI()
app.include_router(ambient.router)
app.include_router(camera.router)
app.include_router(raspberry.router)


@app.on_event('startup')
def startup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    for pin in settings.relay_pins:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
