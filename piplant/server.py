import settings

import RPi.GPIO as GPIO
import uvicorn

from fastapi import FastAPI

from piplant.rest import ambient, raspberry


app = FastAPI()
app.include_router(ambient.router)
app.include_router(raspberry.router)


@app.on_event('startup')
def startup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()


if __name__ == '__main__':
    uvicorn.run('server:app', host=settings.INTERFACE, port=settings.PORT)
