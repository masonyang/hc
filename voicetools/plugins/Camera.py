# -*- coding: utf-8-*-

from __future__ import absolute_import
import os
import subprocess
import time
import sys
import dingdangpath
import socket
import urllib
import urllib2
import json
import requests
import cookielib
import base64

reload(sys)
sys.setdefaultencoding('utf-8')

WORDS = [u"PAIZHAO", u"ZHAOPIAN"]
SLUG = "camera"


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    # sys.path.append(mic.dingdangpath.LIB_PATH)

    quality = 100
    count_down = 3
    dest_path = os.path.expanduser('~/Pictures')
    vertical_flip = False
    horizontal_flip = False
    sound = True
    usb_camera = True
    # read config
    dest_file = os.path.join(dest_path, "%s.jpg" % time.time())
    if usb_camera:
        command = "fswebcam --no-banner -r 1024x765 -q "
        if vertical_flip:
            command = command+' -s v '
        if horizontal_flip:
            command = command+'-s h '
        command = command+dest_file
    else:
        command = ['raspistill', '-o', dest_file, '-q', str(quality)]
        if count_down > 0 and sound:
            command.extend(['-t', str(count_down*1000)])
        if vertical_flip:
            command.append('-vf')
        if horizontal_flip:
            command.append('-hf')
    if sound and count_down > 0:
        mic.say(u"收到，%d秒后启动拍照" % (count_down))
        if usb_camera:
            time.sleep(count_down)

    process = subprocess.Popen(command, shell=usb_camera)
    res = process.wait()
    if res != 0:
        if sound:
            mic.say(u"拍照失败，请检查相机是否连接正确")
        return
    if sound:
        mic.say(dingdangpath.data('audio', 'camera.wav'),True)
        uploadImage(dest_file)

    return True

def isValid(mic,text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["拍照", "拍张照"])

def uploadImage(imagefile):

    ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    data = ip+'|'+imagefile
    base_data = base64.b64encode(data)
    api = serverapi()
    return api.uploadImage(base_data)

class serverapi(object):

    """docstring for Translate"""
    def __init__(self):
        pass

    def getConfig(self):
        
        pass

    def makeUrl(self,url,params):
        return url+params;
        pass

    def request(self,url):
        request = urllib2.Request(url)

        f = urllib2.urlopen(request)

        return f.read()
        pass

    def post(self,url,data):

        req=urllib2.Request(url,data)

        f=urllib2.urlopen(req)

        return f.read()
        pass

    def uploadImage(self,alinfo):

        allowIpConfig = ['192.168.1.100','192.168.1.101','192.168.1.102','192.168.1.103']

        for ip in allowIpConfig:

            url = 'http://'+ip+'/index.php/openapi/bot.homecenter.album/save'

            t = os.system('curl '+url)

            if(t == 0):
                url = url+'?alinfo='+alinfo
                result = self.request(url)

                return True
            pass

        return True
