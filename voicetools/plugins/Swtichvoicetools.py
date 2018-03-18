# -*- coding: utf-8-*-
import sys
import dingdangpath
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')

WORDS = [u"BREAK"]
SLUG = "swtichvoicetools"


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxBot -- wechat robot
    """

    mic.stop_passive = True

    settings = readVoiceToolsSwitchConfig()

    setting['switch'] = 'off'
	setting['server_sync_path'] = settings['server_sync_path']
	setting['server_ip'] = settings['server_ip']
    print(setting)
    setVoiceToolsSwitchConfig(setting)

    mic.say(u"好的，一会见")
    return True

def readVoiceToolsSwitchConfig():

	data_file = os.path.join(dingdangpath.TEMP_PATH, 'voicetools_switch.json')

	f=open(data_file)

	setting = json.load(f)

	return setting

def setVoiceToolsSwitchConfig(result):

	data_file = os.path.join(dingdangpath.TEMP_PATH, 'voicetools_switch.json')

    with open(data_file, 'w') as out_file:
    	json.dump(result, out_file)

    return True

def isValid(mic,text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["休息一下"])