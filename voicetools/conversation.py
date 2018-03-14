#!/usr/bin/env python
# coding: utf-8

import sys
import brain

reload(sys)
sys.setdefaultencoding('utf-8')

class conversation(object):
	"""docstring for conversation"""
	def __init__(self,persona,mic,profile):
		self.mic = mic
		self.persona = persona
		self.profile = profile
		self.brain = brain.Brain(mic, profile)

	def handleForever(self):

		while True:

			if self.mic.stop_passive:
				print("skip conversation for now.")
				time.sleep(1)
				continue

			if not self.mic.stop_passive:
				threshold, transcribed = self.mic.passiveListen(self.persona)
				
				if not transcribed or not threshold:
					print("Nothing has been said or transcribed.")
					continue
				else:
					print("Keyword '%s' has been said!", self.persona)

				input = self.mic.activeListenToAllOptions(threshold)

				if input:
					self.mic.say(input)
					self.brain.query(input,self.mic,self.profile)
				else:
					self.mic.say("什么?")


