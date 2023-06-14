from components import weather_reporter, wine_waiter
import proj_utils
import json

def func_weather_reporter(text):
    
    cityName = '集美区'
    
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
    # print(text)
    
def wine_introduce(text):
    
    ww = wine_waiter.wineWaiter(filepath=proj_utils.WINE_CSV_FILEPATH)
    wn = '长岛冰茶'
    wi = ww.getWine(wn).to_dict()
    print(wi)
    text = ww.wine_introduction_generate(wn,
                                        wi['tag1'][wn],
                                        wi['tag2'][wn],
                                        wi['tag3'][wn],
                                        wi['price'][wn],
                                        )
    print(text)
    ww.tts(text)
    ww.play()