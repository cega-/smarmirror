#!/usr/bin/python
# -*- coding: utf-8 -*-

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import functools

import paho.mqtt.client as mqtt

from multiprocessing import Process, Queue

@asyncio.coroutine
def time(websocket, path, q):
	while True:
		now = datetime.datetime.utcnow().isoformat() + 'Z'
		to_publish = q.get()
		yield from websocket.send('{0}'.format(to_publish))
		#yield from asyncio.sleep(random.random() * 3)

def on_connect(mqttc, obj, flags, rc):
	print("rc: " + str(rc))


def on_message(mqttc, obj, msg, q):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	q.put(msg.payload)


def on_publish(mqttc, obj, mid):
	print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
	print(string)

def launchWS(queue):
	print('IN WS')
	start_server = websockets.serve(functools.partial(time, q=queue), '0.0.0.0', 5678)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()

def launchMQTTReceiver(queue):
	print('IN MQTT')
	mqttc = mqtt.Client()
	mqttc.on_message = functools.partial(on_message, q=queue)
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe
	# Uncomment to enable debug messages
	# mqttc.on_log = on_log
	mqttc.connect("127.0.0.1", 1883, 60)
	mqttc.subscribe("#", 0)

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


