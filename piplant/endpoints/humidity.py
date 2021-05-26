from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from piplant.sensors.dht11 import dht11_sensor as sensor


class HumidTempEndpoint(HTTPEndpoint):

    async def get(self, request):
        return JSONResponse(sensor.get_data())
