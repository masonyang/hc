import base64
from datetime import datetime
import json
import os
import urllib.request

import wave
import webbrowser

import pyaudio
import re

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 8000
CHANNELS = 1
record_second = 5
def record_wav(to_dir=None):
    if to_dir == None:
        to_dir='./'

    pa = pyaudio.PyAudio()

    stream = pa.open(format=FORMAT,
                     channels = CHANNELS,
                     rate = RATE,
                     input=True,
                     frames_per_buffer = CHUNK)

    sava_buffer = []

    for i in range(0,int(RATE/CHUNK*record_second)):
        audio_data = stream.read(CHUNK)
        sava_buffer.append(audio_data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    file_name = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+'.wav'

    file_path = to_dir+file_name


    wf = wave.open(file_path,'wb')
    wf.setframerate(RATE)
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.writeframes(b''.join(sava_buffer))

    wf.close()

    return file_path

def text_open_browser(text):
    url = ""
    if text:
        if len(re.split(u"谷歌",text))>1 or len(re.split('google',text))>1:
            url = 'https://www.google.com'
        elif len(re.split(u'百度',text))>1 or len(re.split('baidu',text))>1:
            url = 'https://www.baidu.com'
    if text != "":
        webbrowser.open_new_tab(url)
    else:
        print('no')

def baiduys(object):
    VOICE_RATE = 8000
    WAVE_FILE = object
    USER_ID = 'joker'
    WAVE_TYPE = 'wav'

    baidu_server = 'https://openapi.baidu.com/oauth/2.0/token?'
    grant_type = 'client_credentials'
    client_id=''
    client_secret = ''

    url = baidu_server+'grant_type='+grant_type+'&client_id='+client_id+'&client_secret='+client_secret

    res = urllib.request.urlopen(url).read()

    data = json.loads(res)

    token = data['access_token']

    with open(WAVE_FILE,'rb') as f:
        fe = f.read()
        speech =  base64.b64encode(fe)
        speech1 = speech.decode('utf-8')

        size = os.path.getsize(WAVE_FILE)


        update = json.dumps({"format":WAVE_TYPE,"rate":VOICE_RATE,"channel":1,'token':token,'cuid':USER_ID,'speech':speech1,'len':size})

        update1 = update.encode('utf-8')

        headers = {'Content-Type':'application/json'}

        url = 'https://vop.baidu.com/server_api'

        req = urllib.request.Request(url,update1,headers)

        r= urllib.request.urlopen(req)


        t= r.read()

        ans =json.loads(t)

        if ans['err_msg']=='success.':
            result = ans['result'][0].encode('utf-8')

            if result!='':
                return result.decode('utf-8')
            else:
                print(u'不存在文件0')
        else:
            print(u'错误')







if __name__ =='__main__':
    to_dir = './'
    file_path = record_wav(to_dir)
    # file_path1 = 'C:\\Users\eexf\PycharmProjects\mcc'+file_path

    # text = baiduys(file_path1)
    # print(text)

    # text_open_browser(text)