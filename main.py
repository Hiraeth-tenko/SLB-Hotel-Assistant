import wave
from components.wav_to_pcm import wav2pcm
from components.SR import Sr
from components.TTS import Tts
from flask import Flask, request
import requests
import proj_utils

app = Flask(__name__)

@app.route('/stt', methods=['POST'])
def stt():
    if request.headers['Content-Type'] == 'audio/wav':
        audio_data = request.data

        with wave.open(proj_utils.RHASSPY_RECV_WAV_FILEPATH, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16-bit 样本宽度
            wav_file.setframerate(16000)  # 采样率为 44100 Hz
            wav_file.writeframes(audio_data)
            print("wav file saved")
        
        wav2pcm(src_path=proj_utils.RHASSPY_RECV_WAV_FILEPATH,
                des_path=proj_utils.RHASSPY_RECV_PCM_FILEPATH)
        
        t = Sr(tid="main.py sr", file=proj_utils.RHASSPY_RECV_PCM_FILEPATH).start()
        while(t.flag == False):
            pass
        msg = t.msg['payload']['result']
        return_msg_back(msg)
        return "success"
    else:
        return "Content-Type is not audio/wav"

@app.route('/tts', methods=['POST'])
def tts():
    text = request.data.decode('utf-8')
    Tts('start text to speech', file=proj_utils.TTS_WAV_FILEPATH).start(text)

    with open(proj_utils.TTS_WAV_FILEPATH, 'rb') as file:
        audio_data = file.read()
    url = 'http://10.22.156.12:12101/api/text-to-speech'  # 目标URL

    headers = {
        'Content-Type': 'audio/wav'
    }
    response = requests.post(url, data=audio_data, headers=headers)

    # 处理响应
    if response.status_code == 200:
        result = response.text
        print(result)
    else:
        print('请求失败')


def return_msg_back(msg):
    url = 'http://10.22.228.8/api/speech-to-text'  # 目标URL

    # 构造请求数据
    data = msg

    # 发送POST请求
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.post(url, data=data, headers=headers)

    # 处理响应
    if response.status_code == 200:
        result = response.text
        print(result)
    else:
        print('请求失败')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
