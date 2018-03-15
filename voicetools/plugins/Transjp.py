# -*- coding: utf-8-*-
# 闲聊插件

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

import sys
import translate

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ["FANYIRIYU","RIYUFANYI"]
SLUG = "transjp"


def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    if not any(word in text for word in [u"结束翻译", u"翻译结束"]):

        if mic.transjp_mode:
            sentence = transJp(text)
            mic.say(sentence,False,'jp')
        else:
            mic.say(u"进入中文翻译日文模式，现在跟我说说话吧")
            mic.transjp_mode = True
            mic.skip_passive = True
    else:
        mic.say(u"退出已开启中文翻译日文模式")
        mic.skip_passive = False
        mic.transjp_mode = False

    return True

def transJp(text):
    trans = translate.Translate()

    sentence = trans.jpTrans(text,'zh')

    return sentence

def isValid(mic,text):
    """
        Returns True if the input is related to weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """

    if mic.transjp_mode:
        return True
    else:
        return any(word in text for word in [u"日语翻译", u"结束翻译", u"翻译结束"])
