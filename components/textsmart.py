import requests
import json
import aliyun_utils


def recognize(text):
    obj = {
        "str": text,
        "options": {
            "input_spec": {"lang": "auto"},
            "word_seg": {"enable": True},
            "pos_tagging": {"enable": True, "alg": "log_linear"},
            "ner": {"enable": True, "alg": "fine.high_acc"}
        }
    }
    req_str = json.dumps(obj).encode()
    r = requests.post(url=aliyun_utils.TEXTSMART_API_URL, data=req_str)
    content = json.loads(r.text.encode())
    # print(r.text)
    return content


def pair(src, des_list: list):
    obj = {
        "text_pair_list": [],
        "options": {"alg": "linkage"},
        "echo_data": {"id": "123"}
    }
    for des in des_list:
        obj["text_pair_list"].append({"str1": src, "str2": des})
    req_str = json.dumps(obj).encode()
    r = requests.post(
        url=aliyun_utils.TEXTSMART_API_MATCH_TEXT_URL, data=req_str)
    content = json.loads(r.text.encode())
    # print(r.text)
    return content
