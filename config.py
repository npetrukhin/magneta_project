# -*- coding: utf-8 -*-
DOMAIN = 'demo.magneta.io'

HTTPS_PROTOCOL = 'https'
WSS_PROTOCOL = 'wss'

TOKEN_PATH = '/api/2/token'
WEBSOCKET_PATH = '/api/2/relay'
REGISTER_PATH = '/api/2/user/register'

APP_ID = 'app'
DEVICE_TYPE = 'android'

# количество подключений
CONNECTIONS_NUMBER = 3

# порт
PORT = 9001


def get_url(protocol, domain, path):
    return '{}://{}{}'.format(protocol, domain, path)













