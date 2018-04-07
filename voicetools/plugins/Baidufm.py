# -*- coding: utf-8-*-
# 百度FM插件
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import base64
import hashlib
import json
import dingdangpath
import random
from urllib import urlopen

reload(sys)
sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(10)

WORDS = ["BAIDUYINYUE"]
SLUG = "baidufm"

DEFAULT_CHANNEL = 13


class MusicPlayer(threading.Thread):

    def __init__(self, playlist,mic):
        super(MusicPlayer, self).__init__()
        self.event = threading.Event()
        self.event.set()
        self.playlist = playlist
        self.idx = 0
        self.is_stop = False
        self.is_pause = False
        self.song_file = "dummy"
        self.mic = mic
        self.directory = tempfile.mkdtemp()

    def run(self):
        while True:
            if self.event.wait():
                self.play()
                if not self.is_pause:
                    self.pick_next()

    def play(self):
        print('MusicPlayer play....')
        song_url = "http://music.baidu.com/data/music/fmlink?" +\
            "type=mp3&rate=320&songIds=%s" % self.playlist[self.idx]['id']
        song_name, song_link, song_size, song_time =\
            self.get_song_real_url(song_url)
        self.pause()
        self.mic.play("即将播放"+song_name)
        self.resume()
        self.download_mp3_by_link(song_link, song_name, song_size)
        self.play_mp3_by_link(song_link, song_name, song_size, song_time)

    def get_song_real_url(self, song_url):
        try:
            htmldoc = urlopen(song_url).read().decode('utf8')
        except:
            return(None, None, 0, 0)

        content = json.loads(htmldoc)

        try:
            song_link = content['data']['songList'][0]['songLink']
            song_name = content['data']['songList'][0]['songName']
            song_size = int(content['data']['songList'][0]['size'])
            song_time = int(content['data']['songList'][0]['time'])
        except:
            print('get real link failed')
            return(None, None, 0, 0)

        return song_name, song_link, song_size, song_time

    def play_mp3_by_link(self, song_link, song_name, song_size, song_time):
        process = subprocess.Popen("pkill play", shell=True)
        process.wait()
        if os.path.exists(self.song_file):
            if not self.is_stop:
                cmd = ['/usr/bin/mplayer', self.song_file]
                print('begin to play')
                with tempfile.TemporaryFile() as f:
                    subprocess.call(cmd, stdout=f, stderr=f)
                    f.seek(0)
                    output = f.read()
                    print(output)
            print('play done')
            if not self.is_pause:
                print('song_file remove')
                os.remove(self.song_file)

    def download_mp3_by_link(self, song_link, song_name, song_size):
        hl = hashlib.md5()
        hl.update(song_name.encode(encoding='utf-8'))
        file_name = hl.hexdigest() + ".mp3"

        self.song_file = os.path.join(self.directory, file_name)
        if os.path.exists(self.song_file):
            return
        print("begin DownLoad %s size %d" % (song_name, song_size))
        mp3 = urlopen(song_link)

        block_size = 8192
        down_loaded_size = 0

        file = open(self.song_file, "wb")
        while True and not self.is_stop:
            try:
                buffer = mp3.read(block_size)

                down_loaded_size += len(buffer)

                if(len(buffer) == 0):
                    if down_loaded_size < song_size:
                        if os.path.exists(self.song_file):
                            os.remove(self.song_file)
                    break
                file.write(buffer)

                if down_loaded_size >= song_size:
                    print('%s download finshed' % self.song_file)
                    break

            except:
                if os.path.getsize(self.song_file) < song_size:
                    print('song_file remove')
                    if os.path.exists(self.song_file):
                        os.remove(self.song_file)
                break

        file.close()

    def pick_next(self):
        self.idx += 1
        if self.idx > len(self.playlist) - 1:
            self.idx = 0

    def pause(self):
        try:
            self.event.clear()
            self.is_pause = True
            subprocess.Popen("pkill play", shell=True)
        except:
            pass

    def resume(self):
        self.is_pause = False
        self.event.set()

    def stop(self):
        self.pause()
        self.is_stop = True
        self.playlist = []
        if os.path.exists(self.song_file):
            os.remove(self.song_file)
        if os.path.exists(self.directory):
            os.removedirs(self.directory)


def get_channel_list(page_url):
    try:
        htmldoc = urlopen(page_url).read().decode('utf8')
    except:
        return {}

    content = json.loads(htmldoc)
    channel_list = content['channel_list']

    return channel_list


def get_song_list(channel_url):
    try:
        htmldoc = urlopen(channel_url).read().decode('utf8')
    except:
        return{}

    content = json.loads(htmldoc)
    song_id_list = content['list']

    return song_id_list


def handle(text, mic, profile):

    channel_config = readBaiduFmSwitchConfig('channel')

    if(channel_config):

        in_dex = random.randint(0,9)

        channel_id = channel_config[in_dex]['channel_id']
        channel_name = channel_config[in_dex]['channel_name']

    else:
        page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
        channel_list = get_channel_list(page_url)

        channel = DEFAULT_CHANNEL

        channel_id = channel_list[channel]['channel_id']
        channel_name = channel_list[channel]['channel_name']

    # page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
    # channel_list = get_channel_list(page_url)

    # channel = DEFAULT_CHANNEL

    # channel_id = channel_list[channel]['channel_id']
    # channel_name = channel_list[channel]['channel_name']
        
    mic.say(u"播放" + channel_name)

    channel_url = 'http://fm.baidu.com/dev/api/' +\
        '?tn=playlist&format=json&id=%s' % channel_id
    song_id_list = get_song_list(channel_url)

    music_player = MusicPlayer(song_id_list,mic)

    music_player.start()

    mic.transjp_mode = True
    mic.fm_mode = True
    mic.skip_passive = True
    persona = ['多啦a梦','哆啦a梦']

    while True:

        switch = readBaiduFmSwitchConfig('switch')

        if switch == 'on':
            try:
                threshold, transcribed = mic.passiveListen(persona)
            except Exception, e:
                logger.error(e)
                threshold, transcribed = (None, None)

            if not transcribed or not threshold:
                print("FM Nothing has been said or transcribed.")
                continue

            music_player.pause()
            input = mic.activeListen()

            if input == "退出电台":
                music_player.stop()
                mic.say(u"退出电台")
                mic.trans_mode = False
                mic.fm_mode = False
                mic.skip_passive = False
                return True
            else:
                mic.say(u"什么？")
                music_player.resume()
                mic.trans_mode = True
                mic.skip_passive = True
                mic.fm_mode = True


def readBaiduFmSwitchConfig(key):

    data_file = os.path.join(dingdangpath.TEMP_PATH, 'baidufm_switch.json')

    f=open(data_file)

    setting = json.load(f)

    return setting[key]

def isValid(mic,text):
    return any(word in text for word in [u"电台",u"退出电台"])