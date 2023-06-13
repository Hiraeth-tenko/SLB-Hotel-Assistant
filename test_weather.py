from components import weather_reporter
import proj_utils
import json

wr = weather_reporter.weatherReporter(filepath=proj_utils.WEATHER_CSV_FILEPATH)
cc = wr.getCityCode('集美区')['adcode']
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
wr.play()
# print(text)

