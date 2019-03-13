#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import datetime
import random
import websockets
 
connected = set()
 
@asyncio.coroutine
def pub_sub(websocket, path):
	global connected
	if path == '/broadcast/read' :        
		connected.add(websocket)
		print("READER "+str(websocket.remote_address)+"    connected")
		while True:
			yield from asyncio.sleep(100)
	elif path == '/broadcast/write' :
		print("WRITER "+str(websocket.remote_address)+"    connected")
		try :
			while True:
				data = yield from websocket.recv()
				print("MULTICAST: "+data)
				still_connected = set()
				for ws in connected :
					if ws.open:
						still_connected.add(ws)
						yield from asyncio.wait([ws.send(data)])
					else:
						print("READER "+str(ws.remote_address)+" disconnected")
				connected=still_connected
		except:
			print("WRITER "+str(websocket.remote_address)+" disconnected")
			 
start_server = websockets.serve(pub_sub, '0.0.0.0', 5678, close_timeout=None)
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()