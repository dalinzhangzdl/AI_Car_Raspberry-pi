#_*_ coding:UTF-8 _*_
# @author: zdl 
# 实现离线语音唤醒和语音识别，实现一些语音交互控制
# voice_robot 实现语音开关控制，语音对话

# 导入SDK包
import snowboydecoder
import sys
import signal
import record_monitor as recordMonitor

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

#  回调函数，语音识别在这里实现
def callbacks():

    global detector
    
    # 语音唤醒后，提示ding两声
    snowboydecoder.play_audio_file()
    snowboydecoder.play_audio_file()

    #  关闭snowboy功能
    detector.terminate()

    #  开启语音识别
    recordMonitor.monitor()

    # 打开snowboy功能
    wake_up()    # wake_up —> monitor —> wake_up

# 热词唤醒    
def wake_up():

    global detector
    
    model = 'yahboom.pmdl'  #  唤醒词为 你好，亚博

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # 唤醒词检测函数，调整sensitivity参数可修改唤醒词检测的准确性
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... please say wake-up word:你好，亚博')

    # main loop
    # 回调函数 detected_callback=snowboydecoder.play_audio_file 
    # 修改回调函数可实现我们想要的功能
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    # 释放资源
    detector.terminate()

if __name__ == '__main__':

    wake_up()
