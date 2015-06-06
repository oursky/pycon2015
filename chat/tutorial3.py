#!/usr/bin/env python

import asyncio
import cgi
import datetime
import websockets


def welcome_msg():
    return "Welcome from server! Time now: {}".format(
            datetime.datetime.now().strftime('%H:%M:%S'))



sockets = []




@asyncio.coroutine
def hello(websocket, path):
    yield from websocket.send(welcome_msg())
    sockets.append(websocket)
    while True:
        msg = yield from websocket.recv()
        if msg is None:
            break
        msg = cgi.escape(msg)
        for s in sockets:
            yield from s.send("New message: " + msg)

    sockets.remove(websocket)




server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
