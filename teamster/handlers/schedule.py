from aiohttp.web import Response, Request

from dao.schedule import ScheduleDAO
from utils.decorators import LoadJson
from schemes import AddScheduleSchema
from errors import UserNotFoundError, DaoUserNotFoundError


class ScheduleHandler:

    def __init__(self, schedule_dao: ScheduleDAO):
        self._schedule_dao = schedule_dao

    @LoadJson(AddScheduleSchema())
    async add_schedule(self, request: Request, data: dict) -> Response:
        """
        add new 
        :param request: http request context
        :param data: user parameters
        :return: aiohttp response
        """
        user_id = request.match_info.get('user_id')

        try:
            await self._schedule_dao.add_schedule(user_id, data)
        except DaoUserNotFoundError:
            raise UserNotFoundError()

        return Response(status=201)
