#!/usr/bin/env python
# coding: utf-8
#https://www.cnblogs.com/jokerspace/p/6685388.html

import sys
import conversation
import mic
import stt

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

	persona = ['多啦a梦','哆啦a梦']

	profile = []

	stt_engine_slug = 'baidu-stt'
	
	stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)
	stt_passive_engine_class = stt_engine_class
	
	micphone = mic.Mic(stt_passive_engine_class.get_passive_instance(),stt_engine_class.get_active_instance())

	conver_sation = conversation.conversation(persona,micphone,profile)
	conver_sation.handleForever()