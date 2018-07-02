import aioredis


class RedisConnection:
    """
    class for connection to redis
    """

    def __init__(self, **settings):
        self._dsn = format('redis://{host}:{port}', **settings)

    async def connect(self, loop) -> None:
        """
        create connection pool
        :param loop: asyncio event loop
        :return:
        """
        self._pool = await aioredis.create_redis_pool(self._dsn, loop=loop)

    async def close(self) -> None:
        """
        close opened connection pool
        :return:
        """
        if self._pool:
            await self._pool.close()

    @property
    def pool(self):
        return self._pool
