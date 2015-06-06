#!/usr/bin/env python

import asyncio
import cgi
import datetime
import websockets


def welcome_msg():
    return "Welcome from server! Time now: {}".format(
            datetime.datetime.now().strftime('%H:%M:%S'))

# ANSWER
#@asyncio.coroutine
#def hello(websocket, path):
#    yield from websocket.send(welcome_msg())

#FIXME
def hello(websocket, path):
    websocket.send(welcome_msg()) #FIXME

server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
