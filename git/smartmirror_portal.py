#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle as smartmirror
import smartmirror_conf_class
import gettext
import logging
import os.path
import setproctitle
import traceback

from bottle import Bottle, route, run, template, request, response, static_file, redirect
from jinja2 import Environment, FileSystemLoader, Template
from os import listdir
from os.path import isfile, join

dir_path = os.path.dirname(os.path.realpath(__file__))
iconf = smartmirror_conf_class.ConfClass('{0}/smartmirror_portal.conf'.format(dir_path))
Conf = iconf.conf

if not os.path.isfile(Conf['log']['file']):
	path, filename = os.path.split(Conf['log']['file'])
	if not os.path.isdir(path) :
		os.makedirs(path)
	open(Conf['log']['file'], 'a').close()


# create logger
logger = logging.getLogger('smartmirror')
logger.setLevel(eval(Conf['log']['debug_level']))

# create console handler and set level to debug
ch = logging.FileHandler(Conf['log']['file'])
ch.setLevel(eval(Conf['log']['debug_level']))

# create formatter
formatter = logging.Formatter(fmt='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

try:
	logger.info('Initialize Smartmirror portal env'.format())
	setproctitle.setproctitle('Smartmirror')
###	IMDB_psg = DBManagement_postgres()
	app = smartmirror.default_app()

#	t = gettext.translation('smartmirror', 'translation', ['fr'], fallback=False)
#	_ = t.ugettext
	env = Environment(loader=FileSystemLoader('{0}/templates'.format(dir_path)), extensions=['jinja2.ext.i18n'])
#	env.install_gettext_translations(t)
	l_templates = env.list_templates(extensions=['tpl'])
	
except Exception as e:
	logger.error(u'-- Init Smartmirror Portal --\n Issue into env init: {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
	raise e

def jsonp(request, dictionary):
	if (request.query.callback):
		return "%s(%s)" % (request.query.callback, json.dumps(dictionary))
	return json.dumps(dictionary)

@smartmirror.route('/web/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='web/')

@smartmirror.post('/')
@smartmirror.get('/')
def W_index():

	d_render = {'page_title': 'Smartmirror - Configuration management tool', 'var_var': ['menu.tpl']}

	response.content_type = 'text/html'
	OTemplate = env.get_template('index.tpl')

	return OTemplate.render(d_render)

try:
	logger.info('Start Smartmirror portal. Listening on http://{0}:{1}/'.format(Conf['webserver']['host'], Conf['webserver']['port']))
	smartmirror.run(app=app, host=Conf['webserver']['host'], port=Conf['webserver']['port'], portal='cherrypy')	
except Exception as e:
	logger.error(u'-- Start Smartmirror Portal --\n Issue into webserver: {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
	ch.close()
	raise e