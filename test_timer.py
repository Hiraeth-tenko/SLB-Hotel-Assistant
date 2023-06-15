import datetime
import re
from components import timer
def text_to_time(text):
    # 匹配早上/中午/下午/晚上
    time_match = re.search(r'(早上|中午|下午|晚上)', text)
    if time_match:
        if time_match.group() == '早上':
            hour = int(chinese_to_arabic(re.search(r'(\S+)(?=点)', text).group()))
            minute_match = re.search(r'((?<=点)\S+)?(?=分)', text)
            if minute_match:
                minute = int(chinese_to_arabic(minute_match.group()))
            else:
                minute = 0
        else:
            hour = int(chinese_to_arabic(re.search(r'(\S+)(?=点)', text).group())) + 12
            minute_match = re.search(r'((?<=点)\S+)?(?=分)', text)
            if minute_match:
                minute = int(chinese_to_arabic(minute_match.group()))
            else:
                minute = 0
        return f'{hour:02d}:{minute:02d}'
    else:
        now = datetime.datetime.now()
        times_match = re.search(r'(小时)', text)
        hours=0
        if times_match:
            hours = int(chinese_to_arabic(re.search(r'(\S+)(?=小时)', text).group()))
        if(hours!=0):
            minutes = re.search(r'((?<=小时)\S+)?(?=分)', text)
            if minutes:
                minute = int(chinese_to_arabic(minutes.group()))
            else:
                minute = 0
        else:
            minutes = re.search(r'(\S+)(?=分钟)', text)
            if minutes:
                minute = int(chinese_to_arabic(minutes.group()))
            else:
                minute = 0
        time_delta = datetime.timedelta(hours=hours, minutes=minute)
        new_time = now + time_delta
        new_hours = new_time.hour
        new_minutes = new_time.minute
        return f'{new_hours:02d}:{new_minutes:02d}'
def chinese_to_arabic(text):
    num_dict = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, "十": 10}
    result = 0
    digit = 1
    i=1
    for char in reversed(text):
        if char in num_dict:
            if(num_dict[char]==10):
                 result=result+num_dict[char]
                 i=i+1
                 if(i==3):
                     i=0
            else:
                result += num_dict[char] * digit
                digit *= 10
                i=i+1
    if(i==3):
        result=(result%10)*digit
        #if()
        i=1
    if (result > 20 and result%10!=0):
        result = result - 10
    return result
def test_time(atime):
    tr =timer.timers()
    tr.set_alarm(atime)
    if tr.alarm_triggered():
        text2= "时间到了该醒了朋友"
        tr.tts(text2)
        i=0
        while(i<3):
            tr.play()
            #print(text2)
            i=i+1
        i==0

def test(text):
    t=text_to_time(text)
    #print(t)
    test_time(t)

