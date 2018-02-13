#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class weather(object):
	"""docstring for weather"""
	def __init__(self):
		pass


	def getWeatherInfo(self):

		weather_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather_fetcher.py')

		os.system('python "%s"' % weather_exe)

		home_air_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home_air_sensor.py')

		os.system('python "%s"' % home_air_exe)

		hadata = {}

		wdata = {}

		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')

		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass

		home_air_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home_air.json')

		try:
			with open(home_air_file, 'r') as in_file:
				hadata = json.load(in_file)
		except IOError:
			pass

		if(wdata['today_temp_hig']):
			text='今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
		else:
			text='今天{today_weather},当前气温{current_temp}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
	
		text = text + '当前室内温度{temp}度，室内湿度{humidity}度.'.format(**hadata)

		tomorrow_temp_hig=float(wdata['tomorrow_temp_hig'])

		tomorrow_temp_low=float(wdata['tomorrow_temp_low'])
		
		otherInfo=''

		if(tomorrow_temp_hig>35):
			otherInfo=" 已经进入高温烘烤模式，注意防暑降温"
		elif(tomorrow_temp_hig>30):
			otherInfo="天气开始热起来"
		elif(tomorrow_temp_low<=0):
			otherInfo="温度已跌破零点，注意防寒保暖，全副武装"

		text = text+otherInfo

		return text


