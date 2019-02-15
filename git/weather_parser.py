#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

url = 'http://api.openweathermap.org/data/2.5/weather'

params = dict(
	q='Paris,fr',
	APPID='2266edad3793720bbd46eea84c35fcfb',
	units='metric',
	lang='fr'
)

resp = requests.get(url=url, params=params)
d_weather = resp.json()

print(d_weather['visibility'])