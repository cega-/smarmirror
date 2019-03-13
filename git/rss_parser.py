#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import lxml.html
import lxml.html.clean
import paho.mqtt.client as mqtt
import pprint

from time import sleep

def html_clear_text(html_text):
	doc = lxml.html.fromstring(html_text)
	cleaner = lxml.html.clean.Cleaner(style=True)
	doc = cleaner.clean_html(doc)
	clean_text = doc.text_content()

	return clean_text

python_rss_url = "https://www.francetvinfo.fr/titres.rss"
l_news = []
l_string_news = ''

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

while True:
	feed = feedparser.parse( python_rss_url )
	for entry in feed['entries']:
		title = html_clear_text(entry['title'].rstrip())
		summary = html_clear_text(entry['summary'].rstrip())
		l_string_news += '<div class=\"news-entry\" style=\"display:none\"> <div class=\"news-entry-title\">{0}</div><div class=\"news-entry-summary\">{1}</div></div>'.format(title, summary)

	print(l_string_news)
	infot = mqttc.publish("widget/news-feed", l_string_news, qos=0)
	infot.wait_for_publish()

	sleep(900)
	l_string_news = ''