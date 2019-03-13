#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import websockets
 
@asyncio.coroutine
def hello():
	websocket = yield from  websockets.connect('ws://localhost:5678/broadcast/write')
	while True:
		name = input("Message ? ")
		yield from  websocket.send(name)
 
asyncio.get_event_loop().run_until_complete(hello())