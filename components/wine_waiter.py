import pandas
import requests
import aliyun_utils
import proj_utils
import numpy as np
from components import TTS, textsmart


class wineWaiter:
    def __init__(self) -> None:
        self.wine_list = pandas.read_csv(proj_utils.WINE_CSV_FILEPATH, header=0)
        self.wine_name_list = np.append(self.wine_list.loc[:, ['winename']].values, 
                                        ["甜心","水银","月光","火星"])
        self.wine_list.set_index('winename', inplace=True)

    def sr(self, filepath):
        pass

    def tts(self, text):
        t = TTS.Tts(tid="wine_waiter_tts",
                    file=proj_utils.WINE_TTS_WAV_FILEPATH)
        t.start(text=text)
        t.wait()

    def play(self):
        from pydub import AudioSegment
        from pydub.playback import play
        sound = AudioSegment.from_wav(proj_utils.WINE_TTS_WAV_FILEPATH)
        play(sound)

    def getWine(self, wineName):
        wineInfo = self.wine_list[self.wine_list.index == wineName]
        return wineInfo
    
    def wine_introduction_generate(self, name, tag1, tag2, tag3, price):
        import random
        formats = [
            "{name}：{tag1}、{tag2}、{tag3}，价格：{price}元。",
            "{name}，它的特点是{tag1}、{tag2}和{tag3}，价格为{price}元。",
            "{name}是一款{tag1}、{tag2}、{tag3}的饮品选择，令人愉悦。价格只需{price}元。",
            "尝试{name}，您会体验到{tag1}、{tag2}和{tag3}的独特组合。价格非常实惠，仅需{price}元。",
            "{name}，这是一款{tag1}、{tag2}、{tag3}的经典之选。它的价格为{price}元。",
        ]
        
        format = random.choice(formats)
        introduction = format.format(
            name=name,
            tag1=tag1,
            tag2=tag2,
            tag3=tag3,
            price=price
        )
        
        return "您好，这是饮品介绍。"+introduction
    
    def wine_name_update(self, wine_name):
        if wine_name == "甜心":
            return "甜心冲击"
        if wine_name == "水银":
            return "水银爆炸"
        if wine_name == "月光":
            return "月光爆裂"
        if wine_name == "火星":
            return "火星爆破"
        return wine_name
    
    def wine_find(self, text):
        wine_name = ""
        content = textsmart.recognize(text)
        for item in content['phrase_list']:
            # print(item['str'], end=', ')
            if item['str'] in self.wine_name_list:
                wine_name = item['str']
                break
        if wine_name == "":
            for item in content['phrase_list']:
                # print(item['str'], end=', ')
                if item['str'] in self.wine_name_list:
                    wine_name = item['str']
                    break
        wine_name = self.wine_name_update(wine_name)
        # print(wine_name)
        return wine_name
