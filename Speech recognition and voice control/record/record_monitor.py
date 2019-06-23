#coding:utf-8

#需要安装pyaudio
import wave
import numpy as np
from pyaudio import PyAudio,paInt16
import time
import Voice_recognition as Voice
NUM_SAMPLES = 2000
global t

chunk = 1024
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
    
def save_wave_file(filename,data):   #save data to filename

    wf = wave.open(filename,'wb')
    wf.setnchannels(1)   #set channel
    wf.setsampwidth(2)  #采样字节  1 or 2
    wf.setframerate(16000)  #采样频率  8K or 16K
    wf.writeframes(b"".join(data))
    wf.close()
    
def Monitor():
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
        data = stream.read(NUM_SAMPLES,exception_on_overflow = False) #add exception para
        #if audioFlag == True:
           # rec.append(data)        #剪切的语音文件
        audioBuffer.append(data)     #录音源文件
        audioData = np.fromstring(data,dtype=np.short) #字符串创建矩阵
        largeSampleCount = np.sum(audioData > 2000)
        temp = np.max(audioData)

        print temp
        if temp > 8000 and t == False:
            t = 1 #开始录音
            print "检测到语音信号，开始录音"
            begin = time.time()
            print temp
        if t:
            end = time.time()
            if end-begin > 5:
                timeFlag = 1 #5s录音结束
            if largeSampleCount > 20:
                saveCount = 4
            else:
                saveCount -=1
            if saveCount <0:
                saveCount =0
            if saveCount >0:
                rec.append(data)
            else:
                if len(rec) >0 or timeFlag:
                    save_wave_file('01.wav',rec)
                    Voice.identify('01.wav')
                    rec = []
                    t = 0
                    timeFlag = 0
    stream.stop_stream()
    stream.close()
    p.terminate()

Monitor()

# recognize command  by file



'''
        if temp >4000 :
            audioFlag = True
            
            print "有语音信号"
        if temp <= 4000:
            if audioFlag == True:
                audioFlag = False
                save_wave_file('01.wav',rec)
                Voice.identify('01.wav')
                rec = []
'''
                
                
            
        
        
    
