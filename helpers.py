# -*- coding: utf-8 -*-
import json
import random
import string

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import urlencode
from tornado import gen

from config import (
    get_url, HTTPS_PROTOCOL, DOMAIN, TOKEN_PATH, REGISTER_PATH, APP_ID,
    DEVICE_TYPE)


def create_message(client_id):
    message_text = ''.join(random.choice(string.lowercase) for _ in range(10))
    message = {
        'type': 'message',
        'content': {
            'message': message_text,
            'client_id': client_id
        }
    }
    return json.dumps(message)


@gen.coroutine
def register_user(alias):
    register_url = get_url(HTTPS_PROTOCOL, DOMAIN, REGISTER_PATH)
    method = 'POST'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    register_params = {
        'id': 0,
        'alias': alias,
        'device_type': DEVICE_TYPE
    }

    register_body = urlencode(register_params)

    http_client = AsyncHTTPClient()
    register_request = HTTPRequest(
        register_url, method, headers, register_body)
    yield http_client.fetch(register_request)


@gen.coroutine
def get_token(alias):
    yield register_user(alias)
    token_url = get_url(HTTPS_PROTOCOL, DOMAIN, TOKEN_PATH)
    method = 'POST'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # формируем запрос на получение токена
    token_params = {
        'alias': alias,
        'app_id': APP_ID
    }
    token_body = urlencode(token_params)
    token_request = HTTPRequest(token_url, method, headers, token_body)

    http_client = AsyncHTTPClient()

    # получаем токен
    response = yield http_client.fetch(token_request)
    token = json.loads(response.body).get('token', None)
    raise gen.Return(token)
