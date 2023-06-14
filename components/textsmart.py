import requests
import json
import aliyun_utils


def textsmart(text):
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
    r = requests.post(url=aliyun_utils.TEXTSMART_URL, data=req_str)
    content = json.loads(r.text.encode())
    # print(r.text)
    return content
