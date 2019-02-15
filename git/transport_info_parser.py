#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import lxml.html
import pprint

regexpNS = "http://exslt.org/regular-expressions"

l_url_transport_info = [{'type': 'metro', 'url': 'https://www.ratp.fr/trafic-metro'},
						{'type': 'rer', 'url': 'https://www.ratp.fr/trafic-rer'},
						{'type': 'bus-tram', 'url': 'https://www.ratp.fr/trafic-bus-tramway'}]

html = requests.get('https://www.ratp.fr/trafic-metro')
doc = lxml.html.fromstring(html.content)

l_event_metro = doc.xpath('//div[@class="infos-trafic__item"]')
for event in l_event_metro:
	print(event.xpath('.//span[re:match(@class, \'ligne1$\')]', namespaces={'re':regexpNS}))
	content = event.xpath('.//p')[0].text_content()
	if len(event.xpath('.//span[@class="metro"]')) > 0:
		print(content)

#pprint.pprint(l_event_metro)