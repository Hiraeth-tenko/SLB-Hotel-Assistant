import pandas
import requests
import aliyun_utils
import proj_utils
import numpy as np
from components import TTS, textsmart


class receptionistWaiter:
    def __init__(self) -> None:
        self.order_list = pandas.read_csv(proj_utils.RECE_CSV_FILEPATH)
        self.wine_list = pandas.read_csv(proj_utils.WINE_CSV_FILEPATH)
        self.wine_list = self.wine_list.loc[:, ['winename']].values
        self.entertainment_list = pandas.read_csv(
            proj_utils.ENTERTAINMENT_CSV_FILEPATH)
        self.entertainment_list = self.entertainment_list.loc[:, [
            '娱乐设施']].values

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

    def answer_wine_list(self):
        pass

    def answer_entertainment_list(self):
        return self.entertainment_list

    def answer_human(self):
        pass
