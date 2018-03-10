#!/usr/bin/env python
# coding: utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class conversation(object):
	"""docstring for conversation"""
	def __init__(self,persona,mic):
		self.mic = mic
		self.persona = persona

	def handleForever(self):

		while True:

			threshold, transcribed = self.mic.passiveListen(self.persona)
			
			# if not transcribed or not threshold:
			# 	print("Nothing has been said or transcribed.")
			# 	continue
			# else:
			# 	print("Keyword '%s' has been said!", self.persona)

			input = self.mic.activeListenToAllOptions(threshold)

			if input:
				print(input)
			else:
				print("什么?")


