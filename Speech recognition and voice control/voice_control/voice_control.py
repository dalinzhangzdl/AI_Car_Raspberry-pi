#_*_ coding:UTF-8 _*_
# @author: zdl 
# voice_control 离线安全唤醒+智能语音控制
# wake-up word is too weakness,need train
# 唤醒词：你好，亚博

import snowboydecoder
import signal
import os
import record_monitor as monitor
import time
global detector

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def callbacks():
    global detector
    snowboydecoder.play_audio_file()
    snowboydecoder.play_audio_file()
    os.system('mplayer %s' % 'music/wake_up.mp3')
    #os.system('mplayer %s' % 'music/voiceControlON.mp3')
    
    detector.terminate()
    #time.sleep(2)
    
    monitor.monitor()  # 语音识别与语音控制
    snowBoy()          # solve audio IOerror    snowBoy->monitor->snowBoy

# snowBoy wake up   
def snowBoy():
    
    global detector
    model = 'yahboom.pmdl'

    # capture SIGINT signal, e.g.
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5,audio_gain=1)  #para the high the better
    print('Listening... please say wake-up word:你好，亚博')

    # main loop
    result = detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

    detector.terminate() # close audio

if __name__ == '__main__':   
    snowBoy()
