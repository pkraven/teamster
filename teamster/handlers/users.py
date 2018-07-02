from aiohttp.web import Response, Request

from dao.users import UsersDAO
from dao.schedule import ScheduleDAO
from utils.decorators import LoadJson
from schemas import CreateUserSchema, ResponseUserSchema
from errors import NotFoundUserError


class UsersHandler:

    def __init__(self, users_dao: UsersDAO, schedule_dao: ScheduleDAO):
        self._users_dao = users_dao
        self._schedule_dao = schedule_dao

    @LoadJson(CreateUserSchema(strict=True))
    async def create_user(self, request: Request, data: dict) -> Response:
        """
        create new user
        :param request: http request context
        :param data: user parameters
        :return: aiohttp response
        """
        await self._users_dao.create_user(**data)

        return Response(status=201)

    async def get_user(self, request: Request) -> Response:
        """
        get user with by id
        :param request: http request context
        :param data: user parameters
        :return: aiohttp response
        """
        user_id = request.match_info.get('user_id')
        user = await self._users_dao.get_user(user_id)
        if not user:
            raise NotFoundUserError()

        schedule = await self._schedule_dao.get_schedule(user_id)

        response_data = ResponseUserSchema().dumps({**user, 'schedule': schedule}).data
        return Response(
            status=200,
            content_type='application/json',
            text=response_data
        )

    async def get_users_list(self, request: Request) -> Response:
        """
        get all users
        :param request: http request context
        :return: aiohttp response
        """
        users = await self._users_dao.get_user_list(user_id)

        response_data = ResponseUserSchema().dumps(users, many=True).data
        return Response(
            status=200,
            content_type='application/json',
            text=response_data
        )
