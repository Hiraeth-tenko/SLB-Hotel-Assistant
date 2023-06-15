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
        self.error = -1

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
        
    def answer_hint(self):
        text = "请使用以下指令："
        for _, row in self.order_list.iterrows():
            text += "想要得知酒店的" + row['name'] + "，请说指令：" + row['order'] + "。"
        return text

    def diff(self, text):
        orders = [row['order'] for _, row in self.order_list.iterrows()]
        res = textsmart.pair(text, orders)
        res_list = res['res_list']
        order = ''
        score = 0
        for i, item in zip(range(len(orders)), res_list):
            if item['score'] > score:
                order = i
                score = item['score']
            # print(item)
        if score < 0.3:
            return self.error
        return order

    def answer_wine_list(self):
        text = "我们酒店提供如下酒水："
        for item in self.wine_list:
            text += item[0] + "，" # type: ignore
        text += "需要了解详情，请说指令：给我介绍一下某某酒水。其中某某酒水为前文提到的酒水名。"
        return text
    
    def answer_entertainment_list(self):
        text = "我们酒店有如下设施："
        for item in self.entertainment_list:
            text += item[0] + "，" # type: ignore
        text += "需要了解详情，请说指令：给我介绍一下某某酒店设施。其中某某酒店设施为前文提到的设施。"
        return text
        
    def answer_human(self):
        text = "好的，已为您呼唤前台服务，请稍等。"
        return text
