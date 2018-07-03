import json
import logging
import time
from aiohttp import web
from aiohttp.web import Response, Request

from dao.users import UsersDAO
from services.redis import RedisConnection
from utils.decorators import LoadJson


logger = logging.getLogger(__name__)


class ChatHandler:

    def __init__(self, redis: RedisConnection, users_dao: UsersDAO) -> None:
        self._redis = redis.pool
        self._users_dao = users_dao

    async def websocket_server(self, request: Request) -> web.WebSocketResponse:
        """
        get websocket message, save and send it to chats
        message: {"action": "send_message", "to_chat": 1, "text": "lalala"}
        :param request: http request context
        :return: websocket response
        """

        chat_id = request.match_info.get('chat_id')
        user_id = request.match_info.get('user_id')

        ws = web.WebSocketResponse(autoclose=False)
        await ws.prepare(request)

        request.app['channels'].setdefault(chat_id, []).append(ws)
        channels = request.app['channels']

        async for msg in ws:
            if msg.type == web.WSMsgType.text:
                try:
                    request_data = json.loads(msg.data)
                    action = request_data['action']
                except Exception:
                    continue

                if action == 'get_last_messages':
                    from_chat = request_data.get('from_chat') if chat_id == 'main' else chat_id
                    if from_chat:
                        await self._get_last_messages(from_chat, ws)

                if action == 'history' and chat_id == 'main':
                    from_chat = request_data.get('from_chat')
                    if from_chat:
                        await self._get_history(from_chat, ws)

                elif action == 'send_message':
                    await self._send_message(channels, request_data, chat_id, user_id)

            elif msg.type == web.WSMsgType.close:
                await self._ws_close(channels[chat_id], ws)
                break

            elif msg.type == web.WSMsgType.error:
                logging.debug(f'websocket connection closed with exception {ws.exception()}')
                await self._ws_close(channels[chat_id], ws)
                break

        return ws

    async def _get_history(self, chat_id: str, ws: web.WebSocketResponse) -> None:
        """
        get all messages
        :param chat_id: chat id
        :param ws: websocket object for send messages
        :return:
        """
        response_data = await self._redis.lrange(chat_id, 0, -1)
        messages = [json.loads(mes) for mes in response_data]
        await ws.send_str(json.dumps(messages))

    async def _get_last_messages(self, chat_id: str, ws: web.WebSocketResponse) -> None:
        """
        get last 10 messages
        :param chat_id: chat id
        :param ws: websocket object for send messages
        :return:
        """
        response_data = await self._redis.lrange(chat_id, -10, -1)
        messages = [json.loads(mes) for mes in response_data]
        await ws.send_str(json.dumps(messages))

    async def _send_message(self, channels: dict, request_data: dict,
                            chat_id: str, user_id: str) -> None:
        """
        send message to current chat and to main chat
        :param channels: all channels dict with ws objects
        :param request_data: received message
        :param chat_id: chat id
        :param user_id: user id
        :return:
        """
        message = {
            'time': time.time(),
            'chat_id': chat_id,
            'user_id': user_id,
            'text': request_data.get('text'),
        }

        to_chat = request_data.get('to_chat')
        if chat_id == 'main' and to_chat:
            chat_id = to_chat

        # save to redis
        await self._redis.rpush(chat_id, json.dumps(message))

        # send message to current chat and main chat
        response_data = json.dumps([message])
        for user in channels.get(chat_id, []):
            await user.send_str(response_data)
        if channels.get('main') and len(channels['main']):
            await channels['main'][0].send_str(response_data)

    @staticmethod
    async def _ws_close(chat_list: list, ws: web.WebSocketResponse) -> None:
        await ws.close()
        logging.debug(f'ws connection closed {ws.closed}')
        chat_list.remove(ws)
