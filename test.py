#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


sayNotice = '半点报时，现在 23:30'

url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(sayNotice)
os.system('/usr/bin/mplayer "' + url+'"')