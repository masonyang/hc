#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime
import json
import time
import weather
import serverapi

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

	def getCurrentDate(self):

		time_now = datetime.datetime.now()
		self.current_date = time_now.strftime('%Y-%m-%d')
		return current_date

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

	def readTemporaryNoticeConfig(self,key):

		data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporarynotice.json')
		
		if os.path.exists(data_file) == False:
			api = serverapi.serverapi()
			api.temporaryNoticePull(data_file)
			time.sleep(60)

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

	#每日提醒任务
	def commonNoticeService(self,full_date_time,full_time_string,hour_minute_string,xingqi):

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
							os.system('/usr/bin/mplayer "' + url+'"')

						if(items['noticeMusic']):
							time.sleep(5)
							os.system('/usr/bin/mplayer "'+items['noticeMusic']+'"')
						if(items['action'] == 'server'):
							if(items['dateType'] == 'reboot'):
								os.system('sudo reboot')
							elif(items['dateType'] == 'shutdown'):
								os.system('sudo shutdown -h now')
			pass

		return True

	#临时任务提醒
	def temporaryNoticeService(self,full_date_time,full_time_string,hour_minute_string,xingqi,current_date):

		autoPullConfig = ['7:45:00','10:00:00','12:00:00','15:00:00','18:00:00','18:30:00','21:00:00','21:30:00','22:00:00']

		input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporarynotice.json')

		if full_time_string in autoPullConfig:
			api = serverapi.serverapi()
			api.temporaryNoticePull(input_file)

		outlineNotice = self.readTemporaryNoticeConfig('outlineNotice')

		if full_time_string in outlineNotice['noticeTimeDot']:
			url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
			u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=1&vol=5&pit=5'.format(outlineNotice['noticeContent'].encode('utf-8'))
			os.system('/usr/bin/mplayer "' + url+'"')

		temporaryNotice = self.readTemporaryNoticeConfig('temporaryNotice')

		for items in temporaryNotice:

			if(items['Date'] == current_date):
				if(items['start_time'] == full_time_string):
					sayNotice = ''
					if(items['sayNotice']):
						sayNotice += items['sayNotice']

					if(items['Description']):
						sayNotice += items['Description']

					url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
					u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=1&vol=5&pit=5'.format(sayNotice.encode('utf-8'))
					os.system('/usr/bin/mplayer "' + url+'"')

					if(items['noticeMusic']):
						time.sleep(5)
						os.system('/usr/bin/mplayer "'+items['noticeMusic']+'"')

			pass

		return True

	def run(self):

		while True:

			xingqi = self.getXingQi()

			full_date_time = self.getFullDateTime()
			
			full_time_string = self.getFullTime()
			
			hour_minute_string = self.getHourMinuteTime()

			current_date = self.getCurrentDate()

			self.commonNoticeService(full_date_time,full_time_string,hour_minute_string,xingqi)#每日提醒服务

			self.temporaryNoticeService(full_date_time,full_time_string,hour_minute_string,xingqi,current_date)#每日提醒服务

		return True
