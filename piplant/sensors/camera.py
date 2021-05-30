import asyncio

from io import BytesIO

from picamera import PiCamera

from fastapi import APIRouter
from fastapi.responses import StreamingResponse


class RaspberryCamera:

    def __init__(self):
        self.camera = PiCamera()

    async def take_photo(self, stream):
        self.camera.start_preview()
        await asyncio.sleep(2)
        self.camera.capture(stream, 'jpeg')


router = APIRouter()
sensor = RaspberryCamera()


@router.get('/camera')
async def get_image():
    stream = BytesIO()
    await sensor.take_photo(stream)
    stream.seek(0)
    return StreamingResponse(stream, media_type='image/jpeg')
