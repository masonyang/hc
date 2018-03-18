# -*- coding: utf-8-*-
import sys

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
    mic.say(u"好的，一会见")
    return True

def isValid(mic,text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["休息一下"])