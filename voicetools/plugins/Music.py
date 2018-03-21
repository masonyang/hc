# -*- coding: utf-8-*-
# 音乐插件

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

import os
import sys
import pygame
import random
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ["MUSIC","YINYUE"]
SLUG = "music"


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
    if not any(word in text for word in ["结束播放"]):

        mp3Index = ('柯南','稻香')

        mp3Music = ('http://mp32.9ku.com/upload/2016/05/27/829218.m4a','http://ar.h5.ra01.sycdn.kuwo.cn/resource/n3/320/74/27/4113470514.mp3')

        mp3MusicList = {'柯南':'http://mp32.9ku.com/upload/2016/05/27/829218.m4a','稻香':'http://ar.h5.ra01.sycdn.kuwo.cn/resource/n3/320/74/27/4113470514.mp3'}
        
        if mic.transjp_mode:

            pygame.mixer.init()

            if text == "播放音乐":

                print('play music')

            if text == "暂停播放":
                pygame.mixer.music.pause()
            elif text == "继续播放":
                pygame.mixer.music.unpause()
            elif text == "换一首":

                if pygame.mixer.music.get_busy() == True:
                    pygame.mixer.music.stop()
                
                in_dex = random.randint(0,1)

                url = mp3Music[in_dex]

                response = urllib2.urlopen()
                
                mp3file = response.read()

                track = pygame.mixer.music.load(mp3file)

                pygame.mixer.music.play()

            else:
                if pygame.mixer.music.get_busy() == True:
                    pygame.mixer.music.stop()

                url = mp3Music[0]

                for ele in mp3Index:
                    if text == ele:
                        url = mp3MusicList[ele]

                response = urllib2.urlopen(url)
                
                mp3file = response.read()

                track = pygame.mixer.music.load(mp3file)

                pygame.mixer.music.play()
        else:
            mic.say("进入动感音乐模式")
            mic.transjp_mode = True
            mic.skip_passive = True
    else:
        pygame.mixer.music.stop()
        pygame.quit()
        mic.say("退出动感音乐模式")
        mic.skip_passive = False
        mic.transjp_mode = False

    return True

def isValid(mic,text):
    """
        Returns True if the input is related to weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """

    if mic.transjp_mode:
        return True
    else:
        return any(word in text for word in ["播放音乐", "结束播放", "暂停播放","继续播放"])
