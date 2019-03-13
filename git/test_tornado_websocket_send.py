#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class Client(object):
	def __init__(self, url, timeout):
		self.url = url
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
			yield self.ws.write_message(msg)

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

if __name__ == "__main__":
	client = Client("ws://127.0.0.1:5678/server", 5)