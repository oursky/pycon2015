#!/usr/bin/env python

import asyncio
import websockets


@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    asyncio.get_event_loop().create_task(display(websocket))

    # Note: This does not work. It is because `input` blocks
    # the event loop.
    #while True:
    #    name = input("Your message: ")
    #    yield from websocket.send(name)
    #    print("> {}".format(name))


@asyncio.coroutine
def display(socket):
    while True:
        msg = yield from socket.recv()
        if msg is None:
            asyncio.get_event_loop().stop()
            break


asyncio.get_event_loop().run_until_complete(hello())
