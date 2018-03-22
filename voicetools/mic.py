# -*- coding: utf-8-*-
from __future__ import absolute_import
import sys
import ctypes
import tempfile
import wave
import audioop
import time
import pyaudio
import mute_alsa
import os
import dingdangpath

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf-8')

class Mic:
    speechRec = None
    speechRec_persona = None

    def __init__(self, passive_stt_engine,
                 active_stt_engine):
        """
        Initiates the pocketsphinx instance.

        Arguments:
        profile -- config profile
        speaker -- handles platform-independent audio output
        passive_stt_engine -- performs STT while Dingdang is in passive listen
                              mode
        acive_stt_engine -- performs STT while Dingdang is in active listen
                            mode
        """
        self.robot_name = '叮当'
        self.passive_stt_engine = passive_stt_engine
        self.active_stt_engine = active_stt_engine

        try:
            asound = ctypes.cdll.LoadLibrary('libasound.so.2')
            asound.snd_lib_error_set_handler(mute_alsa.c_error_handler)
        except OSError:
            pass
        self._audio = pyaudio.PyAudio()
        print("Initialization of PyAudio completed.")
        self.stop_passive = False
        self.skip_passive = False
        self.chatting_mode = False
        self.transjp_mode = False
        self.fm_mode = False
    def __del__(self):
        self._audio.terminate()

    def getScore(self, data):
        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def fetchThreshold(self):

        # TODO: Consolidate variables from the next three functions
        THRESHOLD_MULTIPLIER = 2.5
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(20)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):
            try:
                data = stream.read(CHUNK)
                frames.append(data)

                # save this data point as a score
                lastN.pop(0)
                lastN.append(self.getScore(data))
                average = sum(lastN) / len(lastN)

            except Exception as e:
                print("异常:"+e.message)
                continue

        try:
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print("异常:"+e.message)
            pass

        # this will be the benchmark to cause a disturbance over!
        THRESHOLD = average * THRESHOLD_MULTIPLIER

        return THRESHOLD

    def stopPassiveListen(self):
        """
        Stop passive listening
        """
        self.stop_passive = True

    def passiveListen(self, PERSONA):
        """
        Listens for PERSONA in everyday sound. Times out after LISTEN_TIME, so
        needs to be restarted.
        """

        THRESHOLD_MULTIPLIER = 2.5
        
        RATE = 16000

        CHUNK = 1024

        file_path = os.path.join(dingdangpath.DATA_PATH,'audio/listen_awakekw.wav')

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # number of seconds to listen before forcing restart
        LISTEN_TIME = 10

        CHANNELS = 1
        
        record_second = 5

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(30)]

        didDetect = False

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

            try:
                if self.stop_passive:
                    print('stop passive')
                    break

                data = stream.read(CHUNK)

                # save this data point as a score
                lastN.pop(0)
                lastN.append(self.getScore(data))
                average = sum(lastN) / len(lastN)

                # this will be the benchmark to cause a disturbance over!
                THRESHOLD = average * THRESHOLD_MULTIPLIER

                # flag raised when sound disturbance detected
                didDetect = False
            except Exception as e:
                print("异常:"+e.message)
                pass

        # start passively listening for disturbance above threshold
        for i in range(0, RATE / CHUNK * LISTEN_TIME):

            try:
                if self.stop_passive:
                    print('stop passive')
                    break

                data = stream.read(CHUNK)
                frames.append(data)
                score = self.getScore(data)

                if score > THRESHOLD:
                    didDetect = True
                    break
            except Exception as e:
                print("异常:"+e.message)
                continue

        # print('score:'+bytes(score)+' THRESHOLD:'+bytes(THRESHOLD))

        # no use continuing if no flag raised
        if not didDetect:
            print("没接收到唤醒指令")
            try:
                # self.stop_passive = False
                stream.stop_stream()
                stream.close()
            except Exception as e:
                print("异常:"+e.message)
                pass
            return (None, None)

        # cutoff any recording before this disturbance was detected
        frames = frames[-20:]

        # otherwise, let's keep recording for few seconds and save the file
        DELAY_MULTIPLIER = 1
        for i in range(0, RATE / CHUNK * DELAY_MULTIPLIER):

            try:
                if self.stop_passive:
                    break
                data = stream.read(CHUNK)
                frames.append(data)
            except Exception as e:
                print("异常:"+e.message)
                continue

        # save the audio data
        try:
            # self.stop_passive = False
            stream.stop_stream()
            stream.close()

            wf = wave.open(file_path,'wb')
            wf.setframerate(RATE)
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self._audio.get_sample_size(pyaudio.paInt16))
            wf.writeframes(b''.join(frames))

            wf.close()
        except Exception as e:
            print("异常:"+e.message)
            pass

        transcribed = self.passive_stt_engine.transcribe_keyword(
            ''.join(frames))

        if transcribed is not None and \
           any(transcribed in phrase for phrase in PERSONA):
            return (THRESHOLD, transcribed)

        return (False, transcribed)

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns the first matching string or None
        """

        options = self.activeListenToAllOptions(THRESHOLD, LISTEN, MUSIC)

        return options

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        """
            Records until a second of silence or times out after 12 seconds

            Returns a list of the matching options or None
        """

        RATE = 16000
        CHUNK = 1024
        LISTEN_TIME = 12

        CHANNELS = 1
        
        record_second = 5

        if not self.transjp_mode:
            self.say(dingdangpath.data('audio', 'beep_hi.wav'),True)

        file_path = os.path.join(dingdangpath.DATA_PATH,'audio/listen_content.wav')

        # check if no threshold provided
        if THRESHOLD is None:
            THRESHOLD = self.fetchThreshold()

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        frames = []
        # increasing the range # results in longer pause after command
        # generation
        lastN = [THRESHOLD * 1.2 for i in range(40)]

        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                score = self.getScore(data)

                lastN.pop(0)
                lastN.append(score)

                average = sum(lastN) / float(len(lastN))

                # TODO: 0.8 should not be a MAGIC NUMBER!
                if average < THRESHOLD * 0.8:
                    break
            except Exception as e:
                print("异常:"+e.message)
                continue

        # save the audio data
        try:
            stream.stop_stream()
            stream.close()

            wf = wave.open(file_path,'wb')
            wf.setframerate(RATE)
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self._audio.get_sample_size(pyaudio.paInt16))
            wf.writeframes(b''.join(frames))

            wf.close()
        except Exception as e:
            print("异常:"+e.message)
            pass

        if not self.transjp_mode:
            self.say(dingdangpath.data('audio', 'beep_lo.wav'),True)

        return self.active_stt_engine.transcribe(frames)

    def say(self, phrase, isaudio=False,lang='zh'):
        print(u"机器人说：%s" % phrase)
        self.stop_passive = True

        if(isaudio):
            os.system('/usr/bin/aplay '+phrase)
        else:
            url = 'http://tts.baidu.com/text2audio?idx=1&tex='+phrase.encode('utf-8')+'&cuid=baidu_speech_demo&cod=2&lan='+lang+'&ctp=1&pdt=1&spd=4&per=1&vol=5&pit=5'
            os.system('/usr/bin/mplayer "' + url+'"')

        time.sleep(1)  # 避免叮当说话时误唤醒
        self.stop_passive = False

    def play(self, src):
        # play a voice
        # self.speaker.play(src)
        return True