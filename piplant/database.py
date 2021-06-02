import asyncpg


class ConnectionPool:

    def __init__(self):
        self.pool = None

    async def start(self, **kwargs):
        self.pool = await asyncpg.create_pool(**kwargs)


pool = ConnectionPool()
