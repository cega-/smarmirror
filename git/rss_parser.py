#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import lxml.html
import lxml.html.clean
import pprint

def html_clear_text(html_text):
	doc = lxml.html.fromstring(html_text)
	cleaner = lxml.html.clean.Cleaner(style=True)
	doc = cleaner.clean_html(doc)
	clean_text = doc.text_content()

	return clean_text

python_rss_url = "https://www.francetvinfo.fr/titres.rss"
l_news = []

feed = feedparser.parse( python_rss_url )

for entry in feed['entries']:
	title = html_clear_text(entry['title'].rstrip())
	summary = html_clear_text(entry['summary'].rstrip())
	l_news.append({'title': title, 'summary': summary})

print(l_news)