#_*_ coding:UTF-8 _*_
# @author: zdl
# weather_forecast.py python2.7.13
# 百度云语音合成+Json获取天气预报实现天气预报播报


# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端

from aip import AipSpeech
import os
from urllib import urlopen
from bs4 import BeautifulSoup


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



def taken_weather(city_info):

    city = ''

    if city_info ==  '101010100':
        city = "北京市的天气是："
    elif city_info ==  '101020100':
        city = "上海市的天气是："
    elif city_info ==  '101280101':
        city = "广州市的天气是："
    elif city_info == '101280601':
        city = "深圳市的天气是："
    elif city_info == '101210101':
        city = "杭州市的天气是："
    elif city_info == '101270101':
        city = "成都市的天气是："
    elif city_info == '101110101':
        city = "西安的天气是："
    elif city_info == '101190101':
        city = "南京市的天气是："
    
    url = 'http://www.weather.com.cn/weather/' + city_info + '.shtml'
    
    resp=urlopen(url)
    soup=BeautifulSoup(resp,'html.parser')

    tagToday=soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签

    try:
        temperatureHigh=tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
    except AttributeError as e:
        temperatureHigh=tagToday.find_next('p',class_="tem").span.string  #获取第二天的最高温度代替

    temperatureLow=tagToday.i.string  #获取最低温度
    weather=soup.find('p',class_="wea").string #获取天气

    with open('weather_result.txt','w') as f:
        f.write( city + weather.encode('utf-8')+'，')
        f.write('最低气温是：'+ temperatureLow.encode('utf-8')+ '，')
        f.write('最高气温是：'+ temperatureHigh.encode('utf-8')+'度')
    f.close()
    
def forecast(city_info):
    taken_weather(city_info)
    tts('weather_result.txt')
    os.system('mplayer %s' % 'synthesis.mp3')
    

if __name__ == '__main__':
    
    forecast('101210101')

