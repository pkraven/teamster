from aiohttp.web import Response, Request

from dao.schedule import ScheduleDAO
from utils.decorators import LoadJson
from schemas import AddScheduleSchema
from errors import NotFoundUserError, DaoNotFoundUserError


class ScheduleHandler:

    def __init__(self, schedule_dao: ScheduleDAO):
        self._schedule_dao = schedule_dao

    @LoadJson(AddScheduleSchema(strict=True))
    async def add_schedule(self, request: Request, data: dict) -> Response:
        """
        add new string to schedule
        :param request: http request context
        :param data: schedule string parameters
        :return: aiohttp response
        """
        user_id = int(request.match_info.get('user_id'))

        try:
            await self._schedule_dao.add_schedule(user_id=user_id, **data)
        except DaoNotFoundUserError:
            raise NotFoundUserError()

        return Response(status=201)
