# -*- coding: UTF-8 -*-
# token weather

from urllib import urlopen
from bs4 import BeautifulSoup


resp=urlopen('http://www.weather.com.cn/weather/101280601.shtml')
soup=BeautifulSoup(resp,'html.parser')

tagToday=soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签

try:
    temperatureHigh=tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
except AttributeError as e:
    temperatureHigh=tagToday.find_next('p',class_="tem").span.string  #获取第二天的最高温度代替

temperatureLow=tagToday.i.string  #获取最低温度
weather=soup.find('p',class_="wea").string #获取天气

with open('weather_result.txt','w') as f:
    f.write('深圳的天气是：' + weather.encode('utf-8')+'，')
    f.write('最低气温是：'+ temperatureLow.encode('utf-8')+ '，')
    f.write('最高气温是：'+ temperatureHigh.encode('utf-8'))
f.close()

print('最低温度:' + temperatureLow.encode('utf-8'))
print('最高温度:' + temperatureHigh.encode('utf-8'))
print('天气:' + weather.encode('utf-8'))
