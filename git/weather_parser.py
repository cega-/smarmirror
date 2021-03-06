#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import paho.mqtt.client as mqtt
import requests

from time import sleep

url = 'http://api.openweathermap.org/data/2.5/weather'

params = dict(
	q='Paris,fr',
	APPID='2266edad3793720bbd46eea84c35fcfb',
	units='metric',
	lang='fr'
)

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()
string_weather = ''
d_weather_widget = {}

while True:
	resp = requests.get(url=url, params=params)
	d_weather = resp.json()

	string_weather = """<div id="current_temp"> 
				{0}°C
			</div>
			<div id="forecast_temp">
				{1}°C min / {2}°C max
			</div>
			<div id="logo_weather">
				<i class="wi {3}"></i>
			</div>
			<div id="string_weather">
				{4}
			</div>""".format(int(d_weather['main']['temp']), int(d_weather['main']['temp_min']), int(d_weather['main']['temp_max']), 'wi-owm-{0}'.format(d_weather['weather'][0]['id']), d_weather['weather'][0]['description'].capitalize())

	d_weather_widget['weather_logo'] = '<i class="wi wi-owm-{0}"></i>'.format(d_weather['weather'][0]['id'])
	d_weather_widget['weather_string'] = d_weather['weather'][0]['description'].capitalize()
	d_weather_widget['weather_temp'] = '{0}°C'.format(int(d_weather['main']['temp']))
	d_weather_widget['weather_forcast_temp'] = '{0}°C min / {1}°C max'.format(int(d_weather['main']['temp_min']), int(d_weather['main']['temp_max']))

	infot = mqttc.publish("widget/weather", json.dumps(d_weather_widget), qos=0)
	infot.wait_for_publish()
	
	
	print(string_weather)
	sleep(900)