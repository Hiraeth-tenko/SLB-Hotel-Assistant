import wave
import program
from components.wav_to_pcm import wav2pcm
from components.SR import Sr
from components.TTS import Tts
from flask import Flask, request
import re
import proj_utils
from program import func_weather_reporter
from program import func_ertertianment_introduce
import subprocess

app = Flask(__name__)


@app.route('/stt', methods=['POST'])
def stt():
    if request.headers['Content-Type'] == 'audio/wav':
        audio_data = request.data

        with wave.open(proj_utils.RHASSPY_RECV_WAV_FILEPATH, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16-bit 样本宽度
            wav_file.setframerate(16000)  # 采样率为 16000Hz
            wav_file.writeframes(audio_data)
            print("wav file saved")

        wav2pcm(src_path=proj_utils.RHASSPY_RECV_WAV_FILEPATH,
                des_path=proj_utils.RHASSPY_RECV_PCM_FILEPATH)

        t = Sr(tid="main.py sr", file=proj_utils.RHASSPY_RECV_PCM_FILEPATH)
        t.start()
        t.wait()
        order = t.msg['payload']['result']
        if dispatch(order):
            return "recognition successful"
        else:
            return "recognition failed"
    else:
        return "Content-Type is not audio/wav"


def tts(text):
    Tts('start text to speech', file=proj_utils.TTS_WAV_FILEPATH).start(text)


def dispatch(order):
    pattern = []
    # 识别句子中，是否同时出现了’查询‘和’天气‘
    pattern[1] = r'(?=.*查询)(?=.*天气)'
    # 识别句子中，是否出现了‘介绍’
    pattern[2] = r'介绍(.+)'
    # 识别句子中，是否同时出现了’介绍‘和‘娱乐游戏室’
    pattern[3] = r"(?=.*介绍)(?=.*娱乐游戏室)"
    # 识别句子中的时间，例如：；请在八点四十七叫醒我’，提取出句中的’八点四十七‘
    pattern[4] = r"请在(\S+)叫醒我"

    # 查询天气
    if re.match(pattern[1], order):
        func_weather_reporter(order)
        return True
    # 介绍酒水
    elif re.match(pattern[2], order):
        program.func_wine_introduce(order)
        return True
    # 介绍娱乐设施
    elif re.match(pattern[3], order):
        func_ertertianment_introduce(order)
        return True
    elif re.match(pattern[4], order):
        # 在句子中查找匹配
        match = re.search(pattern, order)
        time = match.group(1)  # 获取匹配到的时间

        return True
    else:
        sentence = "抱歉，我没有听清楚您说的话,请再说一遍"
        Tts('start text to speech', file=proj_utils.TTS_WAV_FILEPATH).start(sentence)
        play_wav_file(proj_utils.TTS_WAV_FILEPATH)

        return False


def play_wav_file(file_path):
    # 使用aplay命令播放wav文件
    subprocess.run(["aplay", file_path])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
