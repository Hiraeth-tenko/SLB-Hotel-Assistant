import pandas
import requests
import random
import playsound
import aliyun_utils
import proj_utils
# import SR
# import TTS
from components import TTS


class weatherReporter:
    def __init__(self, filepath) -> None:
        self.df = pandas.read_csv(filepath, header=0)
        self.df.set_index('cityname', inplace=True)
        # print(self.df.head(5))

    def sr(self, filepath):
        pass

    def tts(self, text):
        t = TTS.Tts(tid="weather_report_tts",
                    file=proj_utils.WEATHER_TTS_WAV_FILEPATH)
        t.start(text=text)
        t.wait()

    def getCityCode(self, cityName):
        citycode = self.df[self.df.index == cityName]
        return citycode

    def getWeatherBycityCode(self, cityCode):
        payload = {
            "key": aliyun_utils.WEATHER_KEY,
            "city": cityCode,
            "extensions": "base",
            "output": "JSON"
        }
        url = aliyun_utils.WEATHER_URL
        r = requests.get(url=url, params=payload)
        return r

    def weather_generate(self, province, city, weather, temperature, winddirection, windpower, humidity):
        formats = [
            "今天{province}省{city}的天气{weather}，气温{temperature}度，风向{winddirection}，风力{windpower}级，湿度{humidity}%。",
            "现在是{province}省{city}，天气{weather}，气温{temperature}度，风向{winddirection}，风力{windpower}，湿度{humidity}%。",
            "{province}省{city}的天气预报：{weather}，气温{temperature}度，风向{winddirection}，风力{windpower}级，湿度{humidity}%。",
            "{province}省{city}当前的天气为{weather}，气温{temperature}摄氏度，风向{winddirection}，风力{windpower}级，湿度{humidity}%。",
            "{province}省{city}今天的天气状况是{weather}，气温约{temperature}度，风向{winddirection}，风力{windpower}，湿度{humidity}%。",
            "天气预报：{weather}，气温约{temperature}度，{winddirection}风{windpower}级，湿度{humidity}%。",
        ]
        
        format = random.choice(formats)
        forecast = format.format(
            province=province,
            city=city,
            weather=weather,
            temperature=temperature,
            winddirection=winddirection,
            windpower=windpower,
            humidity=humidity
        )
        
        return "为您播报当前地区天气，"+forecast
    
    def play(self):
        playsound.playsound(proj_utils.WEATHER_TTS_WAV_FILEPATH)