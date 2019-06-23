#_*_ coding:UTF-8 _*_
# @author: zdl 
#  python2.7.13 
# 实现语音命令监听及语音识别，对语音识别命令进行解码实现AI车的运动控制

import wave
import numpy as np
from pyaudio import PyAudio,paInt16
import time
import shutil  #实现文件copy和cut
import os
import AICarRun as Run
import voice_recognize as voice  # 导入语音识别和语音合成的函数



NUM_SAMPLES = 2000
global t
#global breakRecordFlag

chunk = 1024
# play wav 
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
    
#save data to filename  
def save_wave_file(filename,data):  

    wf = wave.open(filename,'wb')
    wf.setnchannels(1)      #set channel
    wf.setsampwidth(2)      #采样字节  1 or 2
    wf.setframerate(16000)  #采样频率  8K or 16K
    wf.writeframes(b"".join(data))
    wf.close()

# Analysis command  通过操作文件识别命令  
def recognizeCommand(filename):
    enStop = 0
    enRun = 1
    enBack = 2
    enLeft = 3
    enRight = 4
    car_State = 0
    breakRecordFlag=0
    Run.motor_init()
    Run.brake(0)
    file = filename
    f = open(file,'r')
    out = f.read()
    command = out
    f.close()   # close file aviod exception
    print command
    if command.find('向') != -1 and command.find('前') != -1:
        print "向前"
        shutil.copyfile('music/forward.mp3','music/temp.mp3') #copy file
        car_State = 1
    elif command.find('向') != -1 and command.find('后') != -1:
        print "向后"
        shutil.copyfile('music/back.mp3','music/temp.mp3')
        car_State = 2
    elif command.find('左') != -1 and command.find('转') != -1:
        print '左转弯'
        shutil.copyfile('music/turnLeft.mp3','music/temp.mp3')
        car_State = 3
    elif command.find('右') != -1 and command.find('转') != -1:
        print '右转弯'
        shutil.copyfile('music/turnRight.mp3','music/temp.mp3')
        car_State = 4
    elif command.find('拜') != -1:
        breakRecordFlag = 1
        shutil.copyfile('music/turnOff.mp3','music/temp.mp3')
    elif command.find('识') != -1 and command.find('别') != -1 and command.find('错') != -1 and command.find('误') != -1:
        print '语音识别出错'
    else:
        print '指令错误'
        car_State = 0
        shutil.copyfile('music/error.mp3','music/temp.mp3')
    os.system('mplayer %s' % 'temp.mp3')
    #向前
    if car_State == enRun:
        Run.run(2)
        car_State = 0
    #向后
    elif car_State == enBack :
        Run.back(2)
        car_State = 0
    #左转弯
    elif car_State == enLeft :
        Run.left(2)
        car_State = 0
    #右转弯
    elif car_State == enRight :
        Run.right(2)
        car_State = 0
    #stop
    elif car_State == enStop:
        Run.brake(0)
    else:
        Run.brake(0)
    return breakRecordFlag

# baidu SST  check the voice volumn record 5s
def monitor():
    global saveCount
    pa = PyAudio()
    stream = pa.open(format = paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=NUM_SAMPLES)
    print('开始缓存录音')
    audioBuffer = []
    rec = []
    audioFlag = False
    t = False
    while True:
	
        data = stream.read(NUM_SAMPLES,exception_on_overflow = False)
        audioBuffer.append(data)                       #录音源文件
        audioData = np.fromstring(data,dtype=np.short) #字符串创建矩阵
        largeSampleCount = np.sum(audioData > 2000)
        temp = np.max(audioData)
        print temp
        if temp > 3000 and t == False:  #3000 according different mic
            t = 1 #开始录音
            print "检测到语音信号，开始录音"
            begin = time.time()
            print temp
        if t:
            end = time.time()
            if end-begin > 5:
                timeFlag = 1 #5s录音结束
            if largeSampleCount > 20:
                saveCount = 3
            else:
                saveCount -=1
            if saveCount <0:
                saveCount =0
            if saveCount >0:
                rec.append(data)
            else:
                if len(rec) >0 or timeFlag:
                    
                    save_wave_file('music/detected_voice.wav',rec) # 保存检测的语音
                    voice.identify_synthesize('music/detected_voice.wav') # 调用百度语音实现语音识别和语音合成
                    
                    rec = []
                    t = 0
                    timeFlag = 0
                    
                    breakFlag=recognizeCommand('result.txt')  #Analysis command
                    
                    Run.brake(0)
                    Run.gpio_release()
                    
                    if breakFlag == 1:
                        breakFlag = 0
                        break
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print('next awaken,please say wake-up word')
    Run.gpio_release()

# main函数
#if __name__ == '__main__':
    #monitor()



     
                
            
        
        
    
