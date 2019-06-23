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
import voice_recognize as voice  # 导入语音识别和语音合成的函数

global t  

# 采样参数
NUM_SAMPLES = 2000
chunk = 1024

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
 
# 声音检测、高于阈值保存录音并上传实现语音识别 
def Monitor():
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
                        os.system('mplayer %s' % 'synthesis.mp3')	# play synthesis	
                        # 清除缓存
                        rec = []
                        t = 0
                        timeFlag = 0

        except KeyboardInterrupt:
            break
    
    # 释放资源
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
if __name__ == '__main__':
    Monitor()
    
