from components import wine_waiter
import proj_utils
import json

# ww = wine_waiter.wineWaiter(filepath=proj_utils.WINE_CSV_FILEPATH)
# wn = '长岛冰茶'
# wi = ww.getWine(wn).to_dict()
# print(wi)
# text = ww.wine_introduction_generate(wn,
#                                      wi['tag1'][wn],
#                                      wi['tag2'][wn],
#                                      wi['tag3'][wn],
#                                      wi['price'][wn],
#                                      )
# print(text)
# ww.tts(text)
# ww.play()
import program
program.func_wine_introduce('给我介绍一下月光爆裂')