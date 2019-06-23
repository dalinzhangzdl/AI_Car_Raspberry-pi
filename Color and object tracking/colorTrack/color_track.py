# -*-encoding: UTF-8-*-
# color_track.py python2.7
# @author: zdl
# func:实现颜色追踪、寻球、跟随小车


from collections import deque
import cv2
import AICarRun as Run
import motorControl 
import numpy as np
import threading
import time

# car state
enSTOP = 0
enRUN = 1
enBACK = 2
enBALL = 3
global g_CarState
g_CarState = 0

global count

# video init
def stream_init():
    cap = cv2.VideoCapture(0)
    if cap.isOpened == 0:
        print 'camera is error, Please check!'
    else:
        print 'camera ok!'
    return cap

# search contours
def search_contours(image, hsv_lower, hsv_upper):

    img = cv2.GaussianBlur(image, (5,5), 0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    return cnts

# timer
def time_interrupt():

    global timer
    global time_flag
    time_flag = 1
    timer = threading.Timer(0.01, time_interrupt)
    timer.start()

# calculate contour
def calc_contour(img, cnts):
    cnt_feature = [0,0,0,0]
    center = None
    find_flag = 0
    if len(cnts)>0:
        cnt = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        # 计算轮廓的矩并计算轮廓的重心
        M = cv2.moments(cnt)
        try:
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])) # 计算矩
            find_flag = 1
            cnt_feature = [center[0], center[1], int(radius), find_flag]
            cv2.circle(img, (int(x),int(y)),int(radius),(0,255,0),2)  # 绘制轮廓
        except:
            pass
    else:
        find_flag = 0
        cnt_feature = [0,0,0,0]
        
    return cnt_feature  # 返回中心坐标和轮廓半径

# main
if __name__ == '__main__':
    
    global count
    lower_red = np.array([156,43,46])
    upper_red = np.array([175,255,255])
    center_x = 0
    center_y = 0
    count = 50
    cnt_feature = [0,0,0,0]

    # 系统初始化
    Run.motor_init()
    time_interrupt()
    cap = stream_init()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    while (cap.isOpened()):

        ret, frame = cap.read()
        cnts = search_contours(frame, lower_red, upper_red)
        cnt_feature = calc_contour(frame, cnts)
        print cnt_feature

        # 控制状态更新     
        if cnt_feature[3] == 0 :
            
            g_CarState = enSTOP #enBALL

        else:
            # safe area adjusted according to countour area
            if cnt_feature[2] > 6 and cnt_feature[2] < 27:
                center_x = cnt_feature[0]
                center_y = cnt_feature[1]
                g_CarState = enRUN
                
            elif cnt_feature[2] >= 32:
                print 'back'
                g_CarState = enBACK
            else:
                g_CarState = enSTOP
                Run.brake(0)
                print 'safe area'
        print g_CarState

        # timer motor control
        if time_flag == 1:
            time_flag = 0
            if g_CarState == enBACK:
                Run.backforward(45, 45)
            elif g_CarState == enSTOP:
                Run.forward(0, 0)
            elif g_CarState == enRUN:
                motorControl.motor_control(center_x,center_y,60) # PID control
            elif g_CarState == enBALL:
                Run.forward(60,0)
                count -= 1
                if count == 0:
                    count = 20
                    Run.forward(70,70)
            else:
                Run.brake(0)
        else:
            Run.brake(0)

        # display     
        cv2.imshow('image',frame)
        if cv2.waitKey(1) == 27:
            break
        
    # release
    Run.gpio_release()
    cap.release()
    cv2.destroyAllWindows()


        

            
        
    
        
        
        
    
    
