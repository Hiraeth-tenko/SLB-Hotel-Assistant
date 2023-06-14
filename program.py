from components import weather_reporter, wine_waiter, textsmart
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
    
def func_wine_introduce(text):
    ww = wine_waiter.wineWaiter(filepath=proj_utils.WINE_CSV_FILEPATH)
    wn = ww.wine_find(text)
    if wn == "":
        ww.tts("无法识别出酒水的名称，请重试。")
        ww.play
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
        # ww.play()
