import asyncio
import logging
import uvloop
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware

from utils.config import get_config
from services.db import DatabaseConnection
from services.redis import RedisConnection
from dao.users import UsersDAO
from dao.schedule import ScheduleDAO
from handlers.users import UsersHandler
from handlers.schedule import ScheduleHandler
from handlers.chat import ChatHandler
from utils.config import get_config
from utils.log import set_logger_config


set_logger_config()
logger = logging.getLogger(__name__)


async def initialize(app):
    loop = asyncio.get_event_loop()

    config = get_config()

    app['db'] = DatabaseConnection(**config['db'])
    await app['db'].connect(loop)

    app['redis'] = RedisConnection(**config['redis'])
    await app['redis'].connect(loop)

    users_dao = UsersDAO(db=app['db'])
    schedule_dao = ScheduleDAO(db=app['db'])

    user_handler = UsersHandler(users_dao=users_dao, schedule_dao=schedule_dao)
    schedule_handler = ScheduleHandler(schedule_dao=schedule_dao)
    chat_handler = ChatHandler(redis=app['redis'], users_dao=users_dao)

    app.add_routes([web.post('/user/', user_handler.create_user)])
    app.add_routes([web.get('/user/{user_id}', user_handler.get_user)])
    app.add_routes([web.get('/users/', user_handler.get_users_list)])
    app.add_routes([web.post('/user/{user_id}/schedule/', schedule_handler.add_schedule)])

    app.add_routes([web.get('/ws/', chat_handler.websocket_server)])


async def close_db(app):
    await app['db'].close()
    logger.info('Database pool closed')


async def close_redis(app):
    await app['redis'].close()
    logger.info('Redis closed')


def start(argv):
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    app = web.Application(middlewares=[
        normalize_path_middleware(append_slash=True, merge_slashes=True)
    ])

    app.on_startup.append(initialize)
    app.on_cleanup.append(close_db)
    app.on_cleanup.append(close_redis)

    return app
