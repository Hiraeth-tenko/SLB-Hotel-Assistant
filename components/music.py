from playsound import playsound
import random

key_value_pairs = {
    '0': '../倔强.mp3',
    '1': '../温柔.mp3',
}

# 生成一个随机数
random_index = random.randint(0, len(key_value_pairs)-1)
random_key = list(key_value_pairs.keys())[random_index]

def play_music(command):
    if command == "播放音乐":
        #music_file = "../倔强.mp3"
        # 获取随机选择的值
        music_file = key_value_pairs[random_key]
        print(f"随机选择的键值对为: {random_key}: {music_file}")
        print("Playing music...")
        playsound(music_file)
        print("Music playback completed.")

# 主程序传入指令

command = input()

play_music(command)
