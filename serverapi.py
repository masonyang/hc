#!/usr/bin/env python
# coding: utf-8

import sys
import urllib
import urllib2
import json
import requests
import cookielib

reload(sys)
sys.setdefaultencoding('utf-8')

class serverapi(object):

	"""docstring for Translate"""
	def __init__(self):
		pass

	def getConfig(self):
		
		pass

	def makeUrl(self,url,params):
		return url+params;
		pass

	def request(self,url):
		request = urllib2.Request(url)

		f = urllib2.urlopen(request)

		return f.read()
		pass

	def post(self,url,data):

		req=urllib2.Request(url,data)

		f=urllib2.urlopen(req)

		return f.read()
		pass

	def temporaryNoticePull(self,inputfile):

		url = 'http://192.168.1.102/index.php/openapi/bot.homecenter.temporarynotice/push'

		result = self.request(url)

		with open(inputfile,'w') as f:
			f.write(result)

		return True

