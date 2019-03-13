#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

from tornado.options import define, options

define("port", default=5678, help="run on the given port", type=int)


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r"/server", ServerSocketHandler)]
		super(Application, self).__init__(handlers)

class ServerSocketHandler(tornado.websocket.WebSocketHandler):
	waiters = set()
	cache = []
	cache_size = 200

	def get_compression_options(self):
		# Non-None enables compression with default options.
		return {}

	def check_origin(self, origin):
		return True

	def open(self):
		ServerSocketHandler.waiters.add(self)

	def on_close(self):
		ServerSocketHandler.waiters.remove(self)

	@classmethod
	def update_cache(cls, chat):
		cls.cache.append(chat)
		if len(cls.cache) > cls.cache_size:
			cls.cache = cls.cache[-cls.cache_size :]

	@classmethod
	def send_updates(cls, chat):
		logging.info("sending message to %d waiters", len(cls.waiters))
		for waiter in cls.waiters:
			try:
				waiter.write_message(chat)
			except:
				logging.error("Error sending message", exc_info=True)

	def on_message(self, message):
		print('New MESSAGE : {0}'.format(message))
		logging.info("got message %r", message)
		#ServerSocketHandler.update_cache(chat)
		ServerSocketHandler.send_updates(message)


def main():
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()