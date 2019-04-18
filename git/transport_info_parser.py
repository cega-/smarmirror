#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import lxml.html
import lxml.html.clean
import os.path
import paho.mqtt.client as mqtt
import requests
import smartmirror_conf_class
import traceback

from time import sleep

def html_clear_text(html_text):
	doc = lxml.html.fromstring(html_text)
	cleaner = lxml.html.clean.Cleaner(style=True)
	doc = cleaner.clean_html(doc)
	clean_text = doc.text_content()

	return clean_text

'''
Recuperation des environnements et des configurations
'''
dir_path = os.path.dirname(os.path.realpath(__file__))
iconf = smartmirror_conf_class.ConfClass('{0}/smartmirror_portal.conf'.format(dir_path))
Conf = iconf.conf

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()
l_transport = Conf['widget']['transport_info_parser']
regexpNS = "http://exslt.org/regular-expressions"
d_transport_event = {}
l_transport_widget = []
l_string_transport_event = ''

#l_url_transport_info = [{'type': 'metro', 'url': 'https://www.ratp.fr/trafic-metro'},
#						{'type': 'rer', 'url': 'https://www.ratp.fr/trafic-rer'},
#						{'type': 'bus-tram', 'url': 'https://www.ratp.fr/trafic-bus-tramway'}]

#html = requests.get('https://www.ratp.fr/trafic-metro')
#doc = lxml.html.fromstring(html.content)

while True:
	for d_transport_info in l_transport:
		html = requests.get(d_transport_info['url'])
		doc = lxml.html.fromstring(html.content)

		l_line = d_transport_info['line']
		transport_type = d_transport_info['type']

		l_event = doc.xpath('//div[@class="infos-trafic__item"]')
		for event in l_event:
			for line in l_line:
				if event.xpath('.//span[re:match(@class, \'{0}( |$|\n)\')]'.format(line), namespaces={'re':regexpNS}):
	#				print(line)
					line_dest = event.xpath('.//p')[0].text_content()
					event_text = event.xpath('.//p')[1].text_content()
	#			if len(event.xpath('.//span[@class="{0}"]'.format(transport_type))) > 0:
	#				print(content)
					#print(line_dest)
					#print(event_text)
#					d_transport_event['transport_line'] = line
#					d_transport_event['transport_line_dest'] = html_clear_text(line_dest)
#					d_transport_event['transport_event_text'] = html_clear_text(event_text)

#					l_transport_widget.append(d_transport_event.copy())
					l_string_transport_event += '<div class=\"transport-entry\" style=\"display:none\"> <div class=\"transport-entry-title\"><span class=\"picto\"><img src=\"/web/img/transport_logo/{0}.svg\"></span> {1}</div><div class=\"transport-entry-summary\">{2}</div></div>'.format(line, html_clear_text(line_dest), html_clear_text(event_text))

	d_transport_event['transport'] = l_string_transport_event

	print(d_transport_event)
	infot = mqttc.publish("widget/transport", json.dumps(d_transport_event), qos=0)
	infot.wait_for_publish()
#	l_transport_widget = []
	l_string_transport_event = ''

	sleep(600)
