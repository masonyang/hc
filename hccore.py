#!/usr/bin/env python
# coding: utf-8

import os
import sys
import schedule

reload(sys)
sys.setdefaultencoding('utf-8')

class hccore(object):
	"""docstring for hccore"""
	def __init__(self):
		pass

	def run(self):

		schedule_day = schedule.daySchedule()

		schedule_day.run()
		
		pass
