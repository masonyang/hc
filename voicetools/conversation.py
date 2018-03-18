#!/usr/bin/env python
# coding: utf-8

import sys
import brain
import dingdangpath
import json
import os
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class conversation(object):
	"""docstring for conversation"""
	def __init__(self,persona,mic,profile):
		self.mic = mic
		self.persona = persona
		self.profile = profile
		self.brain = brain.Brain(mic, profile)

	def readVoiceToolsSwitchConfig(self,key):

		data_file = os.path.join(dingdangpath.TEMP_PATH, 'voicetools_switch.json')

		f=open(data_file)

		setting = json.load(f)

		return setting[key]

	def handleForever(self):

		while True:

			switch = self.readVoiceToolsSwitchConfig('switch')

			if switch == 'on':
				self.mic.stop_passive = False
			elif switch == 'off':
				self.mic.stop_passive = True

			if self.mic.stop_passive:
				print("skip conversation for now.")
				time.sleep(1)
				continue

			if not self.mic.stop_passive:

				if not self.mic.skip_passive:
					threshold, transcribed = self.mic.passiveListen(self.persona)
					
					if not transcribed or not threshold:
						print("Nothing has been said or transcribed.")
						continue
					else:
						print("Keyword '%s' has been said!", transcribed)
				# else:
				# 	if not self.mic.chatting_mode:
				# 		self.mic.skip_passive = False
				# 	elif not self.mic.transjp_mode:
				# 		self.mic.skip_passive = False

				input = self.mic.activeListenToAllOptions(threshold)

				if input:
					self.brain.query(input)
				else:
					self.mic.say("什么?")


