#!/usr/bin/env python

import asyncio
import datetime
import time
import websockets


def welcome_msg():
    return "Welcome from server! Time now: {}".format(
            datetime.datetime.now().strftime('%H:%M:%S'))

# ANSWER
#@asyncio.coroutine
#def hello(websocket, path):
#    while True:
#        yield from websocket.send(welcome_msg())
#        yield from asyncio.sleep(1)




@asyncio.coroutine
def hello(websocket, path):
    while True:
        yield from websocket.send(welcome_msg())
        time.sleep(5) #FIXME




server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
