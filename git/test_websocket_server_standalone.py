import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {'value': 0}

USERS = set()

def state_event():
	return json.dumps({'type': 'state', 'value': STATE['value']})

def users_event():
	return json.dumps({'type': 'users', 'count': len(USERS)})

@asyncio.coroutine
def notify_state():
	if USERS:       # asyncio.wait doesn't accept an empty list
		message = state_event()
		yield from asyncio.wait([user.send(message) for user in USERS])

@asyncio.coroutine
def notify_users():
	if USERS:       # asyncio.wait doesn't accept an empty list
		message = users_event()
		yield from asyncio.wait([user.send(message) for user in USERS])

@asyncio.coroutine
def register(websocket):
	USERS.add(websocket)
##	yield from notify_users()

@asyncio.coroutine
def unregister(websocket):
	USERS.remove(websocket)
##	yield from notify_users()

@asyncio.coroutine
def counter(websocket, path):
	# register(websocket) sends user_event() to websocket
	print('Websocket')
	yield from register(websocket)
	try:
		yield from websocket.send(state_event())
		while True:
			pass
			message = yield from websocket.recv()
##			data = json.loads(message)
##			if data['action'] == 'minus':
##				STATE['value'] -= 1
##				yield from notify_state()
##			elif data['action'] == 'plus':
##				STATE['value'] += 1
##				yield from notify_state()
##			else:
##				logging.error(
##					"unsupported event: {}", data)
	finally:
		print('End of LOOP')
		yield from unregister(websocket)

asyncio.get_event_loop().run_until_complete(
	websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()