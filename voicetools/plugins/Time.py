# -*- coding: utf-8-*-
import datetime
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

WORDS = [u"TIME", u"SHIJIAN", u"JIDIAN"]
SLUG = "time"


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

    time_now = datetime.datetime.now()
    full_time_string = time_now.strftime('%H:%M:%S')
    mic.say(u"现在时间是 %s " % full_time_string)
    return True

def isValid(mic,text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["时间", "几点"])
