from components import textsmart
import pandas
import proj_utils
import numpy
import time

def wine_error():
    print("没有这个酒")

def wine_name_update(wine_name):
    if wine_name == "甜心":
        return "甜心冲击"
    if wine_name == "水银":
        return "水银爆炸"
    if wine_name == "月光":
        return "月光爆裂"
    if wine_name == "火星":
        return "火星爆破"
    return wine_name

def wine_proc(text):
    wine_name = ""
    content = textsmart.recognize(text)
    for item in content['phrase_list']:
        # print(item['str'], end=', ')
        if item['str'] in wine_name_list:
            wine_name = item['str']
            break
    if wine_name == "":
        for item in content['phrase_list']:
            # print(item['str'], end=', ')
            if item['str'] in wine_name_list:
                wine_name = item['str']
                break
    if wine_name == "":
        wine_error()
    else:
        wine_name = wine_name_update(wine_name)
        print(wine_name)
    return wine_name

# df = pandas.read_csv("assert/hotel/enwine.csv")
# ----init----
df = pandas.read_csv(proj_utils.WINE_CSV_FILEPATH)
wine_name_list = df.loc[:, ['winename']].values
sub_list = wine_name_list
wine_name_list = numpy.append(wine_name_list, ["甜心","水银","月光","火星"])
print(wine_name_list)

# ----proc----
raw_text = "给我介绍一下"
for wine in sub_list:
    text = raw_text+wine[0]
    wine_name = wine_proc(text)
    print("query: {}, return: {}, {}".format(wine[0], wine_name, wine[0] == wine_name))
    time.sleep(1)
    
