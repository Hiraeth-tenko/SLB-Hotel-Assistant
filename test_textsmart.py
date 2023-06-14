from components import textsmart
import pandas
import proj_utils

# df = pandas.read_csv("assert/hotel/enwine.csv")
df = pandas.read_csv(proj_utils.WINE_CSV_FILEPATH)
tl = df.loc[:, ['winename']].values
for item in tl:
    text = "给我介绍一下"+item[0]
    # print(text)
    content = textsmart.textsmart(text)
    phrase_list = content['phrase_list']
    word_list = content['word_list']
    entity_list = content['entity_list']
    print("------------")
    print("word_list:\n", word_list)
    print("----")
    print("phrase_list:\n", phrase_list)
    print("----")
    print("entity_list:\n", entity_list)
    print("------------")