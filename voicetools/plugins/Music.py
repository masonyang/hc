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

        mp3Index = ('稻香','东京','品冠')

        mp3Music = ('/home/pi/masonInPython/hc/static/4113470514.mp3','/home/pi/masonInPython/hc/static/Tokyo_Bon.mp3','/home/pi/masonInPython/hc/static/1200476465.mp3')

        mp3MusicList = {'稻香':'/home/pi/masonInPython/hc/static/4113470514.mp3','东京':'/home/pi/masonInPython/hc/static/Tokyo_Bon.mp3','品冠':'/home/pi/masonInPython/hc/static/1200476465.mp3'}
        
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
                
                in_dex = random.randint(0,2)

                mp3file = mp3Music[in_dex]

                track = pygame.mixer.music.load(mp3file)

                pygame.mixer.music.play()

            else:
                if pygame.mixer.music.get_busy() == True:
                    pygame.mixer.music.stop()

                mp3file = mp3Music[0]

                for ele in mp3Index:
                    if text == ele:
                        mp3file = mp3MusicList[ele]

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
