import threading
import wave

from components.music import play_music
from components.wav_to_pcm import wav2pcm
from components.SR import Sr
from components.TTS import Tts
from flask import Flask, request
import re
import proj_utils
from program import func_wine_introduce, func_hint, func_receptionist
from program import func_weather_reporter
from program import func_ertertianment_introduce
import subprocess

from test_timer import test

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

        # 获取用户语音识别的结果
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
    patterns = []
    # 识别句子中，是否同时出现了’查询‘和’天气‘
    patterns.append(r'(?=.*查询)(?=.*天气)')

    # 识别句子中，是否出现了‘介绍’
    patterns.append(r'介绍(.+)')

    # 识别句子中的时间，例如：；请在八点四十七叫醒我’，提取出句中的’八点四十七‘
    patterns.append(r"请在(\S+)叫醒我")

    # 识别句子中，是否出现了‘指令’
    patterns.append("指令")
    # 识别句子中，是否出现了‘娱乐设施’或‘酒水’或‘呼唤人工’

    patterns.append(r"(娱乐设施|酒水|呼唤人工)")

    # 识别句子中，是否出现了‘播放音乐’
    patterns.append("播放音乐")
    # 查询天气
    if re.match(patterns[0], order):
        func_weather_reporter(order)
        subprocess.run(["aplay", proj_utils.WEATHER_TTS_WAV_FILEPATH])
        return True

    # 介绍娱乐设施或酒水
    elif re.match(patterns[1], order):
        # 介绍酒水
        if func_wine_introduce(order):
            play_wav_file(proj_utils.WINE_TTS_WAV_FILEPATH)
            return True

        # 介绍娱乐设施
        elif func_ertertianment_introduce(order):
            play_wav_file(proj_utils.ENTERTAINMENT_TTS_WAV_FILEPATH)
            return True

    elif re.match(patterns[2], order):
        # 在句子中查找匹配
        match = re.search(patterns[2], order)
        time = match.group(1)  # 获取匹配到的时间
        # 创建子线程
        thread = threading.Thread(target=thread_function(time))
        # 启动子线程
        thread.start()

    elif re.match(patterns[3], order):
        func_hint()
        play_wav_file(proj_utils.RECE_TTS_WAV_FILEPATH)
        return True

    elif re.match(patterns[4], order):
        func_receptionist(order)
        play_wav_file(proj_utils.RECE_TTS_WAV_FILEPATH)
        return True

    elif re.match(patterns[5], order):
        play_music(order)
        return True

    else:
        sentence = "抱歉，我没有听清楚您说的话,能否再说一遍？"
        Tts('start text to speech', file=proj_utils.TTS_WAV_FILEPATH).start(sentence)
        play_wav_file(proj_utils.TTS_WAV_FILEPATH)
        return False


def play_wav_file(file_path):
    # 使用aplay命令播放wav文件
    subprocess.run(["aplay", "-D", "plughw:1,0", file_path])


def thread_function(time):
    test(time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
