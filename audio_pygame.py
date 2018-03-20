#!/usr/bin/env python
# coding: utf-8

import sys
import time
import pygame

reload(sys)
sys.setdefaultencoding('utf-8')

mp3file = '/home/pi/masonInPython/hc/static/Tokyo_Bon.mp3'

pygame.mixer.init()

print('play music')

track = pygame.mixer.music.load(mp3file)

pygame.mixer.music.play()

time.sleep(10)

pygame.mixer.music.pause()

time.sleep(10)

pygame.mixer.music.unpause()

time.sleep(10)

pygame.mixer.music.stop()