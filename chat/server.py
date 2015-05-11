#!/usr/bin/env python

import asyncio
import websockets
import datetime


ANNOUNCE_TIME_INTERVAL = 1


"""
A list of sockets to send messages to.
"""
clients = []


@asyncio.coroutine
def broadcast(msg):
    """
    Send a message to all currently connected clients.
    """
    for socket in clients:
        # Send network message asynchronously.
        yield from socket.send(msg)


@asyncio.coroutine
def announce_time():
    """
    Send a message containing the current time to all clients.

    This function loop infinitely and asynchronously sleep for an interval
    of time before broadcasting the message.
    """
    while True:
        # `time.sleep` is synchronous, which will block the event loop.
        # `asyncio.sleep` is an asynchronous invariant that does
        # not block the event loop.
        yield from asyncio.sleep(ANNOUNCE_TIME_INTERVAL)
        time_now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = "Current time is {}.".format(time_now)

        # `broadcast` is a coroutine function, to schedule the function
        # from execution, use `yield from`.
        yield from broadcast(msg)


def announce_time2():
    """
    Send a message containing the current time to all clients.

    When the message is sent to all clients, this function schedule
    itself to be called by the event main loop after an interval of time.

    This function is not a coroutine because:

    1.  The `call_soon`/`call_later` functions of the event loop
        expects a callback instead of a coroutine object.
    2.  To demonstrate callback style function instead of a coroutine
        style function.
    """
    time_now = datetime.datetime.now().strftime('%H:%M:%S')
    msg = "Current time is {}.".format(time_now)
    loop = asyncio.get_event_loop()

    # `broadcast` function is a coroutine function that returns a coroutine
    # object. `create_task` turns it into a `Task` (a future) that
    # is scheduled to run in the loop.
    loop.create_task(broadcast(msg))

    # Schedule this function to be called again later to achieve a
    # periodically executed function.
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
