import asyncpg


class DatabaseConnection:
    """
    class for connection to postgresql
    """

    def __init__(self, **settings):
        self._dsn = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(**settings)

    async def connect(self, loop) -> None:
        """
        create connection pool
        :param loop: asyncio event loop
        :return:
        """
        self._pool = await asyncpg.create_pool(dsn=self._dsn, loop=loop)

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
