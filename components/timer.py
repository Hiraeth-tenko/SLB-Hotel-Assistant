import datetime
import proj_utils
import playsound
import threading
from components import TTS
import time
class timers:
    def __init__(self):
        self.alarm_time = None
    def sr(self, filepath):
        pass
    def tts(self, text):
        t = TTS.Tts(tid="timer_tts",
                    file=proj_utils.TIMER_TTS_WAV_FILEPATH)
        t.start(text=text)
        t.wait()
    def set_alarm(self, alarm_time):
        self.alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
    def alarm_triggered(self):
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >=self.alarm_time.time():
                return current_time >= self.alarm_time.time()
                break
    def play(self):
        playsound.playsound(proj_utils.TIMER_TTS_WAV_FILEPATH)

