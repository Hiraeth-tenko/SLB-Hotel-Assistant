import time
import threading
import sys
import json
import aliyun_utils
import nls


# 以下代码会根据音频文件内容反复进行一句话识别
class Sr:
    def __init__(self, tid, file):
        self.__th = threading.Thread(target=self.run)
        self.__id = tid
        self.__file = file
        self.__flag = True

    def loadfile(self, filename):
        with open(filename, "rb") as f:
            self.__data = f.read()

    def start(self):
        self.loadfile(self.__file)
        self.__th.start()

    def _on_start(self, message, *args):
        # print("_on_start:{}".format(message))
        pass

    def _on_error(self, message, *args):
        # print("on_error args=>{}".format(args))
        pass

    def _on_close(self, *args):
        # print("on_close: args=>{}".format(args))
        pass

    def _on_result_chg(self, message, *args):
        # print("_on_chg:{}".format(message))
        pass

    def _on_completed(self, message, *args):
        # print("on_completed:args=>{} message=>{}".format(args, message))
        print("on_completed:args=>{} message=>".format(args))
        msg = json.loads(message)
        print(msg['payload'])
        # if (msg['payload']['result'] == m_utils.wakeup_word):
        #     self.__flag = False
        #     print("Wake up")

    def run(self):
        # print("thread:{} start..".format(self.__id))

        sr = nls.NlsSpeechRecognizer(
            url=aliyun_utils.URL,
            token=aliyun_utils.ACCESS_TOKEN,
            appkey=aliyun_utils.ACCESS_APPKEY,
            on_start=self._on_start,
            on_result_changed=self._on_result_chg,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
            callback_args=[self.__id]
        )
        # cnt = int(5)
        # while True:
        if True:
            # while cnt > 0 and self.__flag == True:

            print("{}: session start".format(self.__id))
            r = sr.start(aformat="pcm")

            self.__slices = zip(*(iter(self.__data),) * 640)
            for i in self.__slices:
                sr.send_audio(bytes(i))
                time.sleep(0.01)
            # cnt -= 1
            r = sr.stop()
            print("{}: sr stopped:{}".format(self.__id, r))


def generate(filepath):
    t = Sr(tid="recognize pcm file", file=filepath)
    t.start()


if __name__ == '__main__':
    nls.enableTrace(False)
    # while(True):
    filepath = "path"  # pcm格式录音文件地址
    generate(filepath)