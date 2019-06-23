#coding: utf-8
# AI car motor drive
# @author: zdl

import RPi.GPIO as GPIO
import time
import threading

#电机引脚定义
AIN1 = 6
AIN2 = 13
BIN1 = 26
BIN2 = 19

# RGB led
LED_R = 7
LED_G = 8
LED_B = 25

#设置速度
RunSpeed = 80
TurnSpeed = 60
#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)
#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化操作
def motor_init():
    GPIO.setmode(GPIO.BCM)
    global pwm_ENA1
    global pwm_ENA2
    global pwm_ENB1
    global pwm_ENB2
    global pwm_rled
    global pwm_gled
    global pwm_bled
    #初始化GPIO引脚
    GPIO.setup(AIN1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(AIN2,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(BIN1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(BIN2,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    #初始化PWM频率
    pwm_ENA1 = GPIO.PWM(AIN1,2000)
    pwm_ENA2 = GPIO.PWM(AIN2,2000)
    pwm_ENB1 = GPIO.PWM(BIN1,2000)
    pwm_ENB2 = GPIO.PWM(BIN2,2000)
    pwm_rled = GPIO.PWM(LED_R, 1000)
    pwm_gled = GPIO.PWM(LED_G, 1000)
    pwm_bled = GPIO.PWM(LED_B, 1000)
    pwm_ENA1.start(0)
    pwm_ENA2.start(0)
    pwm_ENB1.start(0)
    pwm_ENB2.start(0)
    pwm_rled.start(0)
    pwm_gled.start(0)
    pwm_bled.start(0)

#car Forward
def run(delaytime):
    pwm_ENA1.ChangeDutyCycle(0)
    pwm_ENA2.ChangeDutyCycle(RunSpeed)
    pwm_ENB1.ChangeDutyCycle(0)
    pwm_ENB2.ChangeDutyCycle(RunSpeed)
    time.sleep(delaytime)
    
#car Reverse
def back(delaytime):
    pwm_ENA1.ChangeDutyCycle(RunSpeed)
    pwm_ENA2.ChangeDutyCycle(0)
    pwm_ENB1.ChangeDutyCycle(RunSpeed)
    pwm_ENB2.ChangeDutyCycle(0)
    time.sleep(delaytime)

#car right
def right(delaytime):
    pwm_ENA1.ChangeDutyCycle(0)
    pwm_ENA2.ChangeDutyCycle(TurnSpeed)
    pwm_ENB1.ChangeDutyCycle(TurnSpeed)
    pwm_ENB2.ChangeDutyCycle(0)
    time.sleep(delaytime)

#car left
def left(delaytime):
    pwm_ENA1.ChangeDutyCycle(TurnSpeed)
    pwm_ENA2.ChangeDutyCycle(0)
    pwm_ENB1.ChangeDutyCycle(0)
    pwm_ENB2.ChangeDutyCycle(TurnSpeed)
    time.sleep(delaytime)

#car stop
def brake(delaytime):
    pwm_ENA1.ChangeDutyCycle(100)
    pwm_ENA2.ChangeDutyCycle(100)
    pwm_ENB1.ChangeDutyCycle(100)
    pwm_ENB2.ChangeDutyCycle(100)
    time.sleep(delaytime)

def forward(Rduty, Lduty):
    # add span func
    if Rduty < 0:
        Rduty = -Rduty
        pwm_ENA1.ChangeDutyCycle(Rduty)
        pwm_ENA2.ChangeDutyCycle(0)
        pwm_ENB1.ChangeDutyCycle(0)
        pwm_ENB2.ChangeDutyCycle(Lduty)
    elif Lduty < 0:
        Lduty = -Lduty
        pwm_ENA1.ChangeDutyCycle(0)
        pwm_ENA2.ChangeDutyCycle(Rduty)
        pwm_ENB1.ChangeDutyCycle(Lduty)
        pwm_ENB2.ChangeDutyCycle(0)
    else:
        pwm_ENA1.ChangeDutyCycle(0)
        pwm_ENA2.ChangeDutyCycle(Rduty)
        pwm_ENB1.ChangeDutyCycle(0)
        pwm_ENB2.ChangeDutyCycle(Lduty)
def backforward(Rduty, Lduty):
    pwm_ENA1.ChangeDutyCycle(Rduty)
    pwm_ENA2.ChangeDutyCycle(0)
    pwm_ENB1.ChangeDutyCycle(Lduty)
    pwm_ENB2.ChangeDutyCycle(0)

def color_led_pwm(iRed, iGreen, iBlue):
    v_red = (100*iRed)/255
    v_green = (100*iGreen)/255
    v_blue = (100*iBlue)/255
    pwm_rled.ChangeDutyCycle(v_red)
    pwm_gled.ChangeDutyCycle(v_green)
    pwm_bled.ChangeDutyCycle(v_blue)
    time.sleep(0.02)

def gpio_release():
    pwm_ENA1.stop()
    pwm_ENA2.stop()
    pwm_ENB1.stop()
    pwm_ENB2.stop()
    GPIO.cleanup()


if __name__ == '__main__':

    try:
        motor_init()
        time.sleep(2)
        print 'right'
        forward(80, 40)
        time.sleep(5)
        backforward(0,0)
        print 'left'
        forward(40,95)
        time.sleep(5)
        backforward(0,0)
    except KeyboardInterrupt:
        gpio_release()
        pass

    
    
    


    

