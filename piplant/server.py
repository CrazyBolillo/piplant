import settings

import uvicorn

from piplant.endpoints.humidity import HumidTempEndpoint

from sensors import dht11

from starlette.applications import Starlette
from starlette.routing import Route


app = Starlette(debug=True, on_startup=dht11.startup(), routes=[
    Route('/dht11', HumidTempEndpoint)
])

if __name__ == '__main__':
    uvicorn.run('server:app', host=settings.INTERFACE, port=settings.PORT)
