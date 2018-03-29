# -*- coding: utf-8-*-
# 百度FM插件
import json
import os
import sys
import dingdangpath

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["SHAIRPLAY"]
SLUG = "shairplay"


def handle(text, mic, profile):

    mic.trans_mode = True
    mic.fm_mode = True
    mic.skip_passive = True
    persona = ['多啦a梦','哆啦a梦']

    os.system('/usr/local/bin/shairplay --apname=无线播放器')

    while True:

        switch = readBaiduFmSwitchConfig('switch')

        if switch == 'on':
            try:
                threshold, transcribed = mic.passiveListen(persona)
            except Exception, e:
                logger.error(e)
                threshold, transcribed = (None, None)

            if not transcribed or not threshold:
                print("Shairplay Nothing has been said or transcribed.如要开启/关闭语音，请去后台百度语音开关操作")
                continue

            input = mic.activeListen()

            if any(word in input for word in [u"关闭无线播放器",u"关闭无限播放器"]):
                os.system('killall /usr/local/bin/shairplay')
                mic.say(u"关闭无线播放器")
                mic.trans_mode = False
                mic.fm_mode = False
                mic.skip_passive = False
                return True


def readBaiduFmSwitchConfig(key):

    data_file = os.path.join(dingdangpath.TEMP_PATH, 'baidufm_switch.json')

    f=open(data_file)

    setting = json.load(f)

    return setting[key]

def isValid(mic,text):
    return any(word in text for word in [u"开启无线播放器",u"开启无限播放器",u"关闭无线播放器",u"关闭无限播放器"])