#_*_ coding:UTF-8 _*_
# @author: zdl
# weather_forecast.py python2.7.13
# 百度云语音合成+Json获取天气预报实现天气预报播报


# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端

from aip import AipSpeech
import os
from urllib2 import urlopen
import json


''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '11472625'
API_KEY = 'NYIvd23qqGAZ1ZPpVpCthENs'
SECRET_KEY = 'DcQWQ9HVc0sqoD091gFxWiCP1i0oNa6u'

# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 将本地文件进行语音合成
def tts(filename):
    f = open(filename,'r')
    command = f.read()
    if len(command) != 0:
        word = command
    f.close()
    result  = client.synthesis(word,'zh',1, {
        'vol': 5,'per':0,
    })
	
# 合成正确返回audio.mp3，错误则返回dict 
    if not isinstance(result, dict):
        with open('synthesis.mp3', 'wb') as f:
            f.write(result)
        f.close()
        print 'tts successful'



def taken_weather():
    ApiUrl= \
        "http://www.weather.com.cn/data/cityinfo/101280601.html"
    html = urlopen(ApiUrl)
    #读取并解码
    data=html.read().decode("utf-8")
    #将JSON编码的字符串转换回Python数据结构
    ss=json.loads(data)
    info=ss['weatherinfo']

    '''
    # 打印天气信息
    for key in info.keys():
        print key
        print info[key]
    '''
    # 将天气信息存储
    with open('weather_result.txt','w') as f:
        f.write('深圳的天气是：' + info['weather'].encode('utf-8')+'，')
        f.write('最低气温是：'+ info['temp1'].encode('utf-8') + '，')
        f.write('最高气温是：'+ info['temp2'].encode('utf-8'))
    f.close()
    
def forecast():
    taken_weather()
    tts('weather_result.txt')
    os.system('mplayer %s' % 'synthesis.mp3')
    

if __name__ == '__main__':
    
    forecast()

