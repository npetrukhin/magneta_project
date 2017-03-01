# -*- coding: utf-8 -*-
from uuid import uuid4

from tornado import gen, web
from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect
from tornado.httputil import url_concat

from config import (DOMAIN, WSS_PROTOCOL, WEBSOCKET_PATH, CONNECTIONS_NUMBER,
                    PORT, get_url)
from helpers import create_message, get_token


@gen.coroutine
def create_websocket_connection(url, alias):
    conn = yield websocket_connect(url)
    global count

    while True:
        message = create_message(alias)
        conn.write_message(message)

        yield gen.sleep(1)

        count += 1


@gen.coroutine
def get_future(alias, wss_url):
    token = yield get_token(alias)
    websocket_url = url_concat(wss_url, {'token': token})
    (yield create_websocket_connection(websocket_url, alias))


@gen.coroutine
def open_websockets(connections_number):
    aliases = [str(uuid4()) for _ in xrange(connections_number)]

    wss_url = get_url(WSS_PROTOCOL, DOMAIN, WEBSOCKET_PATH)

    futures = [get_future(a, wss_url) for a in aliases]

    for f in futures:
        yield f


class MainHandler(web.RequestHandler):
    def get(self):
        global count
        response = {'messages_sent': count}
        self.write(response)


if __name__ == '__main__':
    count = 0
    open_websockets(CONNECTIONS_NUMBER)
    application = web.Application([(r"/", MainHandler)])
    application.listen(PORT)
    IOLoop.current().start()
