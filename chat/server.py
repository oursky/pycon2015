#!/usr/bin/env python

import asyncio
import websockets
import datetime


ANNOUNCE_TIME_INTERVAL = 1
clients = []


@asyncio.coroutine
def broadcast(msg):
    for socket in clients:
        yield from socket.send(msg)


@asyncio.coroutine
def announce_time():
    while True:
        yield from asyncio.sleep(ANNOUNCE_TIME_INTERVAL)
        time_now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = "Current time is {}.".format(time_now)
        yield from broadcast(msg)


# no coroutine for callbacks
def announce_time2():
    time_now = datetime.datetime.now().strftime('%H:%M:%S')
    msg = "Current time is {}.".format(time_now)
    loop = asyncio.get_event_loop()
    loop.create_task(broadcast(msg))
    loop.call_later(ANNOUNCE_TIME_INTERVAL, announce_time2)


@asyncio.coroutine
def hello(websocket, path):
    yield from broadcast("Welcome our new user.")
    clients.append(websocket)
    try:
        while True:
            msg = yield from websocket.recv()
            if msg is None:
                break
            yield from broadcast(msg)
    finally:
        clients.remove(websocket)


start_server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().create_task(announce_time())
asyncio.get_event_loop().call_soon(announce_time2)
asyncio.get_event_loop().run_forever()
