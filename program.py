from components import weather_reporter, wine_waiter, entertainment
import proj_utils
import json
import pandas

def func_weather_reporter(text):
    
    cityName = '翔安区'
    
    wr = weather_reporter.weatherReporter(filepath=proj_utils.WEATHER_CSV_FILEPATH)
    cc = wr.getCityCode(cityName)['adcode']
    # print(cc)
    content =  json.loads(wr.getWeatherBycityCode(cc).content.decode())['lives'][0]
    text = wr.weather_generate(content['province'], 
                        content['city'], 
                        content['weather'], 
                        content['temperature'], 
                        content['winddirection'], 
                        content['windpower'], 
                        content['humidity'])
    wr.tts(text)
    # wr.play()
    print(text)

# 回复酒水列表

# 回复娱乐设施列表

def func_wine_introduce(text) -> bool:
    ww = wine_waiter.wineWaiter()
    wn = ww.wine_find(text)
    if wn == "":
        text = "无法识别出酒水的名称，请重试。"
        print(text)
        ww.tts(text)
        return False
    else:
        wi = ww.getWine(wn).to_dict()
        # print(wi)
        text = ww.wine_introduction_generate(wn,
                                            wi['tag1'][wn],
                                            wi['tag2'][wn],
                                            wi['tag3'][wn],
                                            wi['price'][wn],
                                            )
        print(text)
        ww.tts(text)
        return True

def func_ertertianment_introduce(text) -> bool:
    # text 介绍一下酒店的 xxx （景点）
    et = entertainment.entertainmentWaiter()
    area = et.diff(text)
    # print(area)
    if area == et.error:
        text = "无法识别出娱乐设施，请重试"
        print(text)
        et.tts(text)
        return False
    else:
        text = et.entertainment_introduction_generate(area)
        print(text)
        et.tts(text)
        return True
        