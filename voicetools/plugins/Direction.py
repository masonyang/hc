# -*- coding: utf-8-*-
# 路线查询
import sys
import os
import re
import json, urllib
from urllib import urlencode

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["XIANLU"]
SLUG = "direction"

def request(url, params):
    params = urlencode(params)

    f = urllib.urlopen("%s?%s" % (url, params))

    content = f.read()
    return json.loads(content)

def handle(text, mic, profile):

    mic.say(u'去哪里')

    mic.fm_mode = True

    app_key = 'tzWgCACxPuNInF9LxklKVea3miAclbuf'

    city = '上海'

    or_igin,distine = fenxiText(text)

    print(or_igin+'___'+distine)

    origin = suggestion(or_igin,mic,city,app_key)

    if origin == True:
        return True

    destination = suggestion(distine,mic,city,app_key)

    if destination == True:
        return True

    url_direction = "http://api.map.baidu.com/direction/v2/transit"
    params_direction = {
        "origin" : origin,
        "destination" : destination,
        "page_size" : 1,
        "ak" : app_key,
    }

    res = request(url_direction, params_direction)
    if res:
        status = res["status"]
        if status == 0:
            if len(res['result']['routes']) > 0:
                direction = ""
                for step in res['result']['routes'][0]['steps']:
                    direction = direction + step[0]["instructions"] + "."
                    result = place_name + u"参考路线:" + direction
                mic.say(result)
                mic.fm_mode = False
                return True
            else:
                mic.say(u"导航错误")
                mic.fm_mode = False
                return True
        else:
            mic.say(u"导航接口:" + res['message'])
            mic.fm_mode = False
            return True
    else:
        mic.say(u"导航接口调用失败")
        mic.fm_mode = False
        return True

def fenxiText(text):
    PATTERN = ur'([\u4e00-\u9fa5]{1,10}?(?:到))([\u4e00-\u9fa5]{1,10}?(?:怎么走)){0,3}'

    # data = '新疆维吾尔到伊犁州怎么走'

    data_utf8 = text.decode('utf8')

    pattern = re.compile(PATTERN)

    m = pattern.search(data_utf8)

    if m.lastindex >= 1:
        origin = m.group(1).replace('到','')
    if m.lastindex >= 2:
        distine = m.group(2).replace('怎么走','')

    return origin,distine

def suggestion(keyword,mic,city,app_key):
    url_place = "http://api.map.baidu.com/place/v2/suggestion"
    params_place = {
        "query" : keyword,
        "region" : city,
        "city_limit" : "true",
        "output" : "json",
        "ak" : app_key,
    }

    res = request(url_place, params_place)

    print(res)

    if res:
        status = res["status"]
        if status == 0:
            if len(res['result']) > 0:
                place_name = res['result'][0]["name"]
                return "%f,%f" % (res['result'][0]["location"]['lat'], res['result'][0]["location"]['lng'])
            else:
                mic.say(u"错误的位置")
                mic.fm_mode = False
                return True
        else:
            mic.say(u"位置接口:" + res['message'])
            mic.fm_mode = False
            return True
    else:
        mic.say(u"位置接口调用失败")
        mic.fm_mode = False
        return True


def isValid(mic,text):
    if text.find('怎么走') == -1:
        return False
    else:
        return True