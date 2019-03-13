#!/usr/bin/python
# -*- coding: utf-8 -*-

# WS server that sends messages at random intervals

import datetime
import json
import functools

import paho.mqtt.client as mqtt

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

from time import sleep
from multiprocessing import Process, Queue


class Client(object):
	def __init__(self, url, timeout, queue):
		self.url = url
		self.queue = queue
		self.timeout = timeout
		self.ioloop = IOLoop.instance()
		self.ws = None
		self.connect()
		PeriodicCallback(self.keep_alive, 20000).start()
		self.ioloop.start()

	@gen.coroutine
	def connect(self):
		print("trying to connect")
		try:
			self.ws = yield websocket_connect(self.url)
		except Exception as e:
			print ("connection error")
		else:
			print ("connected")
			self.reader()
			self.sender()

	@gen.coroutine
	def sender(self):
		while True:
			msg = self.queue.get()
			yield self.ws.write_message(json.dumps(msg))

	@gen.coroutine
	def reader(self):
		while True:
			msg = yield self.ws.read_message()
			if msg is None:
				print ("connection closed")
				self.ws = None
				break

	def keep_alive(self):
		if self.ws is None:
			self.connect()
		else:
			self.ws.write_message("keep alive")


def on_connect(mqttc, obj, flags, rc):
	print("rc: " + str(rc))


def on_message(mqttc, obj, msg, q):
	print("MQTT: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	d_msg_info = {'topic': msg.topic, 'content': msg.payload.decode('utf-8')}
	q.put(d_msg_info)


def on_publish(mqttc, obj, mid):
	print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
	print(string)

def launchWS(queue):
	print('IN WS')
	client = Client("ws://127.0.0.1:5678/server", 5, queue)

def launchMQTTReceiver(queue):
	print('IN MQTT')
	mqttc = mqtt.Client()
	mqttc.on_message = functools.partial(on_message, q=queue)
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe
	mqttc.max_queued_messages_set(1)
	# Uncomment to enable debug messages
	# mqttc.on_log = on_log
	mqttc.connect("127.0.0.1", 1883, 60)
	mqttc.subscribe("widget/#", 0)

	mqttc.loop_forever()

q = Queue()

pWS = Process(target=launchWS, args=(q,))
pMQTTReceiver = Process(target=launchMQTTReceiver, args=(q,))

pWS.start()
pMQTTReceiver.start()

#mqttc = mqtt.Client()
#mqttc.on_message = on_message
#mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
#mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
#mqttc.connect("127.0.0.1", 1883, 60)
#mqttc.subscribe("#", 0)

#mqttc.loop_forever()

'''
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
	yield from notify_users()

@asyncio.coroutine
def unregister(websocket):
	USERS.remove(websocket)
	yield from notify_users()

@asyncio.coroutine
def counter(websocket, path):
	# register(websocket) sends user_event() to websocket
	yield from register(websocket)
	try:
		yield from websocket.send(state_event())
		while True:
			message = yield from websocket.recv()
			data = json.loads(message)
			if data['action'] == 'minus':
				STATE['value'] -= 1
				yield from notify_state()
			elif data['action'] == 'plus':
				STATE['value'] += 1
				yield from notify_state()
			else:
				logging.error(
					"unsupported event: {}", data)
	finally:
		yield from unregister(websocket)

asyncio.get_event_loop().run_until_complete(
	websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()
'''