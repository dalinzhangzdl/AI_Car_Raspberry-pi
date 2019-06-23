#_*_ coding:UTF-8 _*_
# @author: zdl 
# snowboy demo代码分析
# 使用snowboy离线唤醒实现控制LED灯
# reference: http://docs.kitt.ai/snowboy/#my-trained-model-works-well-on-laptops-but-not-on-pi-s

# 导入SDK包
import snowboydecoder
import sys
import signal
from light import Light 

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def own_callbacks():
    LED.blink()

'''
# 判断命令行执行指令是否传入唤醒词模型，无则退出程序
if len(sys.argv) == 1: 
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)
'''
# 唤醒词模型为输入的参数，这里可以进行修改
#model = sys.argv[1]
model = 'resources/snowboy.umdl'  # 修改model，指定其文件名

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# 唤醒词检测函数，调整sensitivity参数可修改唤醒词检测的准确性
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.8)
print('Listening... Press Ctrl+C to exit')

LED = Light(7) 

# main loop
# 回调函数 detected_callback=snowboydecoder.play_audio_file 
# 修改回调函数可实现我们想要的功能
detector.start(detected_callback=own_callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

# 释放资源
detector.terminate()

