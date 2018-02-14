#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime
import json
import time
import weather

reload(sys)
sys.setdefaultencoding('utf-8')

class daySchedule(object):
	"""docstring for daySchedule"""
	def __init__(self):
		pass

	def getDate(self):

		time_now = datetime.datetime.now()
		self.xingqi = [1,2,3,4,5,6,0][time_now.isoweekday() - 1]
		self.current_date = time_now.strftime('%Y-%m-%d')
		time_tomorrow = datetime.datetime.now()+86400
		self.tomorrow_date = time_tomorrow.strftime('%Y-%m-%d')
		return True

	def getXingQi(self):

		time_now = datetime.datetime.now()
		xingqi = [1,2,3,4,5,6,0][time_now.isoweekday() - 1]
		return xingqi

	def getFullTime(self):

		time_now = datetime.datetime.now()
		full_time_string = time_now.strftime('%H:%M:%S')
		return full_time_string

	def getHourMinuteTime(self):

		time_now = datetime.datetime.now()
		hour_minute_string = time_now.strftime('%H:%M')
		return hour_minute_string

	def getFullDateTime(self):

		time_now = datetime.datetime.now()
		full_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
		return full_time

	def readDayScheduleConfig(self,key):

		data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dayschedule.json')
		
		f=open(data_file)

		setting = json.load(f)

		return setting[key]

	def isHoliday(date,holidaylist,day):
		holidayResult={}
		weekEndButWork={}

		for i in holidaylist:
			for d in i.get('holiday'):
				for t in d.get('list'):
					if(t.get('status')=='1'):
						holidayResult[t.get('date')] = t.get('date')
					else:
						weekEndButWork[t.get('date')] = t.get('date')

		if(holidayResult.has_key(date)):
			return True
		else:
			if((day==5) or (day==6)):
				return True
			else:
				return False

	def getWeatherInfo(self):

		weatherinfo = weather.weather()

		return weatherinfo.getWeatherInfo()

	def noticeService(self,full_date_time,full_time_string,hour_minute_string,xingqi):

		commonNotice = self.readDayScheduleConfig('commonNotice')

		for items in commonNotice:
			if(items['scheduleType'] == 'notice_everyday'):#每日提醒任务
				if xingqi in items['timeSlot']:#依周几和时间点为判断
					if full_time_string in items['timeDot']:# list 
						if(items['sayNotice']):

							if(items['action']=='timebroadcast'):
								items['sayNotice'] = items['sayNotice'] + hour_minute_string
							elif(items['action']=='weatherbroadcast'):
								items['sayNotice'] = self.getWeatherInfo()

							url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
							u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=1&vol=5&pit=5'.format(items['sayNotice'].encode('utf-8'))
							# os.system('/usr/bin/mplayer "' + url+'"')
							# time.sleep(5)
						if(items['noticeMusic']):
							os.system('/usr/bin/mplayer "%s"' % items['noticeMusic'])
			pass

		return True

	def run(self):

		while True:

			xingqi = self.getXingQi()

			full_date_time = self.getFullDateTime()
			
			full_time_string = self.getFullTime()
			
			hour_minute_string = self.getHourMinuteTime()

			self.noticeService(full_date_time,full_time_string,hour_minute_string,xingqi)#每日提醒服务


		return True
