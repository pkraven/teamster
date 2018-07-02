from aiohttp.web import Response, Request

from dao.users import UsersDAO
from utils.decorators import LoadJson


class ChatHandler:

    def __init__(self, redis, users_dao: UsersDAO):
        self._users_dao = users_dao

    async def websocket_server(self, request: Request) -> Response:
        """
        chat
        :param:
        :return:
        """

        return Response(status=200)
