import pandas
import requests
import aliyun_utils
import proj_utils
import numpy as np
from components import TTS, textsmart


class receptionistWaiter:
    def __init__(self, filepath) -> None:
        pass

    def sr(self, filepath):
        pass

    def tts(self, text):
        t = TTS.Tts(tid="wine_waiter_tts",
                    file=proj_utils.RECE_TTS_WAV_FILEPATH)
        t.start(text=text)
        t.wait()

    def play(self):
        from pydub import AudioSegment
        from pydub.playback import play
        sound = AudioSegment.from_wav(proj_utils.RECE_TTS_WAV_FILEPATH)
        play(sound)
