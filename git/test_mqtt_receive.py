#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
	if rc == 0 :
		print("connected ok")

def on_subscribe(client, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, obj, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = mqtt.Client("python1")             #create new instance 
client.on_connect = on_connect  #bind call back function
client.on_message = on_message        #attach function to callback
client.on_subscribe = on_subscribe
client.connect('127.0.0.1')               #connect to broker
client.subscribe("#") #subscribe
#client.loop_start()  #Start loop 
#time.sleep(4) # Wait for connection setup to complete
##Other code here
client.loop_forever()    #Stop loop 

'''

import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("#", 0)

mqttc.loop_forever()