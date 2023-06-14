import pandas
import requests
import aliyun_utils
import proj_utils
from components import TTS


class wineWaiter:
    def __init__(self, filepath) -> None:
        self.df = pandas.read_csv(filepath, header=0)
        self.df.set_index('winename', inplace=True)
        # print(self.df.head(5))

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
        wineInfo = self.df[self.df.index == wineName]
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
