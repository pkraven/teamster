import json

from aiohttp.web import HTTPException


class ApplicationError(HTTPException):
    status_code = 500

    def __init__(self, messages=None):
        super().__init__(text=json.dumps(messages),
                         content_type='application/json')


class HttpRequestError(ApplicationError):
    status_code = 400


class JSONParseError(HttpRequestError):
    def __init__(self):
        super().__init__({
            'code': 'json_parse_error',
            'detail': "JSON object is expected"
        })


class NoBodyError(HttpRequestError):
    def __init__(self):
        super().__init__({
            'code': 'empty_body',
            'detail': "Body is expected"
        })


class UnprocessableEntityError(ApplicationError):
    status_code = 422

    def __init__(self, exception):
        messages = exception.messages
        super().__init__({
            'errors': messages
        })


class NotFoundUserError(ApplicationError):
    status_code = 404

    def __init__(self):
        super().__init__({
            'code': 'user_not_found',
            'detail': "User not found"
        })


class DaoNotFoundUserError(Exception):
    pass
