import json
import logging
from marshmallow import ValidationError

from errors import (
    NoBodyError,
    JSONParseError,
    UnprocessableEntityError
)


class LoadJson:
    def __init__(self, schema):
        self._schema = schema

    def __call__(self, func):
        async def wrapper(handler, request, *args, **kwargs):
            if not request.body_exists:
                raise NoBodyError()

            body = await request.read()

            try:
                loaded = json.loads(body.decode())
                data = self._schema.load(loaded).data
            except (json.decoder.JSONDecodeError, UnicodeDecodeError, ValueError):
                raise JSONParseError()
            except ValidationError as e:
                raise UnprocessableEntityError(e)

            return await func(handler, request, *args, **kwargs, data=data)

        return wrapper
