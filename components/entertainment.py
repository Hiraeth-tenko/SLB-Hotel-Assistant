import pandas
import requests
import aliyun_utils
import proj_utils
import numpy as np
from components import TTS, textsmart


class entertainmentWaiter:
    def __init__(self) -> None:
        self.facility_list = pandas.read_csv(
            proj_utils.ENTERTAINMENT_CSV_FILEPATH)
        self.facility_name_list = self.facility_list.loc[:, ['娱乐设施']].values
        self.facility_list.set_index('娱乐设施', inplace=True)
        self.threshold = 0.7
        self.key_list = []
        for name in self.facility_name_list:
            self.key_list.append("介绍一下酒店的"+name[0])
        self.error = -1

    def sr(self, filepath):
        pass

    def tts(self, text):
        t = TTS.Tts(tid="wine_waiter_tts",
                    file=proj_utils.ENTERTAINMENT_TTS_WAV_FILEPATH)
        t.start(text=text)
        t.wait()

    def play(self):
        from pydub import AudioSegment
        from pydub.playback import play
        sound = AudioSegment.from_wav(
            proj_utils.ENTERTAINMENT_TTS_WAV_FILEPATH)
        play(sound)

    def diff(self, text):
        res = textsmart.pair(text, self.key_list)
        res_list = res['res_list']
        name = ''
        score = 0
        for i, item in zip(self.facility_name_list,res_list):
            if item['score'] > score:
                name = i
                score = item['score']
        if score < 0.3:
            return self.error
        return name[0]
    
    def entertainment_introduction_generate(self, name):
        facility = self.facility_list[self.facility_list.index == name].to_dict()
        text = '以下是我们酒店'+name+'的介绍。'+facility['介绍'][name]
        return text
