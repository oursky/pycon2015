#!/usr/bin/env python

import aiohttp
import asyncio
import cgi
import datetime
import websockets


def welcome_msg():
    return "Welcome from server! Time now: {}".format(
            datetime.datetime.now().strftime('%H:%M:%S'))



sockets = []




@asyncio.coroutine
def cat_html():
    # Fetch cat html with image asynchronously
    resp = yield from aiohttp.request('GET',
            'http://thecatapi.com/api/images/get?format=html')
    return (yield from resp.text())




@asyncio.coroutine
def handle_msg(websocket, msg):
    # Find cat if client asked for `cat`
    if msg == 'cat':
        yield from websocket.send("Your cat is on the way.")
        output = yield from cat_html()
    else:
        output = "New message: " + msg

    # Broadcast `output` to all clients
    for s in sockets:
        yield from s.send(output)






@asyncio.coroutine
def hello(websocket, path):
    yield from websocket.send(welcome_msg())
    sockets.append(websocket)
    while True:
        msg = yield from websocket.recv()
        if msg is None:
            break
        msg = cgi.escape(msg)
        yield from handle_msg(websocket, msg)
    sockets.remove(websocket)




server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
