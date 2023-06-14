import wave
from components.wav_to_pcm import wav2pcm
from components.SR import Sr
from components.TTS import Tts
from flask import Flask, request
import re
import proj_utils
from program import func_weather_reporter

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
        
        t = Sr(tid="main.py sr", file=proj_utils.RHASSPY_RECV_PCM_FILEPATH)
        t.start()
        t.wait()
        order = t.msg['payload']['result']
        dispatch(order)

        return "success"
    else:
        return "Content-Type is not audio/wav"


def tts():
    text = request.data.decode('utf-8')
    Tts('start text to speech', file=proj_utils.TTS_WAV_FILEPATH).start(text)

def dispatch(order):
    pattern = r'(?=.*查询)(?=.*天气)'
    matches = re.findall(pattern, order)
    if matches:
        func_weather_reporter(order)
    else:
        print('未找到匹配')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
