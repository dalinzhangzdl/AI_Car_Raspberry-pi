#_*_ coding:UTF-8 _*_
# @author: zdl 
# record_monitor
# 实现对声音信号的检测和录音。设置声音强度阈值，高于该阈值截取之后的5s录音数据并对数据进行切片合成并保存为单通道，16K频率的wav文件
# 调用百度语音识别的API接口，对检测到的语音进行识别和合成形成txt文本及MP3文件，便于实现其他功能。
# 需要安装的工具 pyaudio、百度语音python-SDK mplayer


# 导入包
import wave
import numpy as np
from pyaudio import PyAudio,paInt16
import time
import os
import RPi.GPIO as GPIO
import voice_recognize as voice  # 导入语音识别和语音合成的函数
import weather_forecast as weather
import tts as tts

global t

# RGB灯引脚定义
LED_R = 7
LED_G = 8
LED_B = 25

# GPIO设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 初始化GPIO引脚
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

# 采样参数
NUM_SAMPLES = 2000
chunk = 1024

# switch LED
def LED_light(switch):
    if switch == True:
        GPIO.output(LED_R, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.HIGH)
        GPIO.output(LED_B, GPIO.HIGH)
    else:
        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_G, GPIO.LOW)
        GPIO.output(LED_B, GPIO.LOW)        
        
# 播放wav文件
def play(filename):
    wf = wave.open(filename,'rb')
    p = PyAudio()
    stream = p.open( format=p.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)
    while True:
        data = wf.readframes(chunk)
        if data == "":break
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

# 保存wav文件	
def save_wave_file(filename,data):  
	# 语音识别需要保存的格式为 单声道、双字节、16K频率
    wf = wave.open(filename,'wb')
    wf.setnchannels(1)   #set channel
    wf.setsampwidth(2)  #采样字节  1 or 2
    wf.setframerate(16000)  #采样频率  8K or 16K
    wf.writeframes(b"".join(data))
    wf.close()

# 获取文本控制命令并实现控制
def voice_control(filename):
    file = filename
    f = open(file,'r')
    command = f.read()
    f.close()  # close file aviod IOException
    print command

    if command.find('开') != -1 and command.find('灯') != -1:
        #print '开灯'
        LED_light(True)
        os.system('mplayer %s' % 'music/lightOn.mp3')
    elif command.find('关') != -1 and command.find('灯') != -1:
        #print '关灯'
        LED_light(False)
        os.system('mplayer %s' % 'music/lightOff.mp3')
    elif command.find('天') != -1 and command.find('气') != -1:
        if command.find('北') != -1 and command.find('京') != -1:
            weather.forecast('101010100')
        elif command.find('上') != -1 and command.find('海') != -1:
            weather.forecast('101020100')
        elif command.find('广') != -1 and command.find('州') != -1:
            weather.forecast('101280101')
        elif command.find('深') != -1 and command.find('圳 ') != -1:
            weather.forecast('101280601')
        elif command.find('杭') != -1 and command.find('州') != -1:
            weather.forecast('101210101')
        elif command.find('成') != -1 and command.find('都') != -1:
            weather.forecast('101270101')  
        elif command.find('西') != -1 and command.find('安') != -1:
            weather.forecast('101110101')
        elif command.find('南') != -1 and command.find('京') != -1:
            weather.forecast('101190101')
            
    elif command.find('放') != -1 and command.find('音') != -1 and command.find('乐') != -1:
        try:
            os.system('mplayer %s' % 'music/小跳蛙.mp3')
        except KeyboardInterrupt:
            pass
    elif command.find('自') != -1 and command.find('我') != -1 and command.find('介') != -1 and command.find('绍') != -1:
        tts.tts('我是小博，我能说会道，是机器人界的网红段子手，哈哈哈.')
        os.system('mplayer %s' % 'synthesis.mp3')
    elif command.find('编') != -1 and command.find('程') != -1 and command.find('语') != -1 and command.find('言') != -1:
        tts.tts('我不喜欢编程')
        os.system('mplayer %s' % 'synthesis.mp3')
    elif command.find('去') != -1 and command.find('打') != -1 and command.find('球') != -1 :
        tts.tts('打个毛球啊，我要好好学习，走上人生巅峰。')
        os.system('mplayer %s' % 'synthesis.mp3')
    elif command.find('几') != -1 and command.find('岁') != -1:
        tts.tts('哼，我不想告诉你。')
        os.system('mplayer %s' % 'synthesis.mp3')
    else:
        os.system('mplayer %s' % 'synthesis.mp3')      
 
# 声音检测、高于阈值保存录音并上传实现语音识别 
def monitor():

    LED_light(False)
    print "声音检测实现语音识别和合成，Press Ctrl+C to exit "
    pa = PyAudio()  # 实例化pyaudio
    stream = pa.open(format = paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=NUM_SAMPLES)
    print('开始缓存录音')
	
	# 初始化缓存数组
    audioBuffer = []
    rec = []
	# 初始化标志位
    audioFlag = False
    t = False
    while True:
        try:
            # 读取采样音频并获取特征信息
            data = stream.read(NUM_SAMPLES,exception_on_overflow = False) #add exception para
            audioBuffer.append(data)     #录音源文件
            audioData = np.fromstring(data,dtype=np.short) #字符串创建矩阵
            largeSampleCount = np.sum(audioData > 2000)  # 采样变量
            temp = np.max(audioData)    # 获取声音强度
            print temp
		
            if temp > 8000 and t == False:  # 设置声音检测阈值，需根据麦克风适当调整
                t = 1  #  开始录音
                print "检测到语音信号，开始录音"
                begin = time.time()
                print temp
			
            if t:
                end = time.time()
                if end-begin > 5:
                    timeFlag = 1 #  5s录音结束
                if largeSampleCount > 20:
                    saveCount = 4
                else:
                    saveCount -=1
                if saveCount <0:
                    saveCount =0
                if saveCount >0:
                    rec.append(data)  # 合成数据
                else:
                    if len(rec) >0 or timeFlag:
				
                        save_wave_file('detected_voice.wav',rec) # 保存检测的语音
                        voice.identify_synthesize('detected_voice.wav') # 调用百度语音实现语音识别和语音合成
                        #os.system('mplayer %s' % 'synthesis.mp3')	# play synthesis
                        voice_control('result.txt')
                        # 清除缓存
                        rec = []
                        t = 0
                        timeFlag = 0
                        break

        except KeyboardInterrupt:
            break
    
    # 释放资源
    stream.stop_stream()
    stream.close()
    pa.terminate()

'''   
if __name__ == '__main__':
    monitor()
'''
