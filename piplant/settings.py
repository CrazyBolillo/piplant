from starlette.config import Config

config = Config('.env')

DATABASE_URL = config('DATABASE_URL', cast=str, default='mongodb://localhost:27017')
SESSION_TIMEOUT = config('SESSION_TIMEOUT', cast=int, default='900')
INTERFACE = config('INTERFACE', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8000)
DHT11_PIN = config('DHT11_PIN', cast=int, default=26)
