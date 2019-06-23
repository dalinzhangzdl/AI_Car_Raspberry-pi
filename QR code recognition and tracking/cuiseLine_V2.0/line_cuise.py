#encoding: utf-8
#cuiseline

# use roi
# @author:zdl

import cv2
import numpy as np
import time
import math
import threading
#import motorControl as PIDControl
#import AICarRun as Run

# 定时器 修改para实现定时不同时间
def time_interrupt():
    global timer
    global s_flag
    s_flag = 1
    timer = threading.Timer(0.01,time_interrupt)
    timer.start() 

#画白色十字光标
def drawCross(img,mid_x,mid_y,size):
    cv2.line(img,
             (mid_x-int(size/2),mid_y),
             (mid_x+int(size/2),mid_y),
             (255,255,255),
             2)
    cv2.line(img,
             (mid_x,mid_y-int(size/2)),
             (mid_x,mid_y+int(size/2)),
             (255,255,255),
             2)
#寻找颜色块，并绘制直边界矩形
#def searchColorBlocks(img, roi, hsv_lower, hsv_upper, Xoffset, Yoffset):
def searchColorBlocks(img, roi, Xoffset, Yoffset):

    blocks_feature = [0,0,0,0]
    
    #mask = cv2.inRange(roi,hsv_lower,hsv_upper)
    
    mask=cv2.erode(roi,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #print(len(cnts))
    
    #获取外接矩形
    if len(cnts)>0:
        cnt = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        cnt_area = cv2.contourArea(cnt)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(img,(x+Xoffset,y+Yoffset),(x+w+Xoffset,y+h+Yoffset),(255,0,0),2)
        drawCross(img,x+w/2+Xoffset,y+Yoffset+h/2,20)
        blocks_feature = [x+w/2+Xoffset, y+Yoffset+h/2, 1, cnt_area]
        #return (x+w/2+Xoffset,y+Yoffset+h/2) 
    else:
        
        blocks_feature = [0, 0, 0, 0]
        print blocks_feature
    return blocks_feature
    # return mid point
    
#打开摄像头
def main():
    global s_flag
    #lower_black = np.array([0,0,0])
    #upper_black = np.array([180,255,46])
    weight_list_F = [0.6, 0.3, 0.1] 
    weight_list_N = [0.5, 0.5]
    
    cap = cv2.VideoCapture(0)
    #Run.motor_init()
    time_interrupt()
    if not cap.isOpened():
        print "camera is error, Please check"
    else:
    #修改分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        while True:
            ret,frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret,th = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)# +cv2.THRESH_OTSU)
            cv2.imshow('th', th)
            
            '''
            #颜色空间处理
            bgr = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            #取ROI
            roi_A = hsv[200:240,20:300]
            roi_B = hsv[100:140,20:300]
            roi_C = hsv[20:60,20:300]
            '''
            # 二值化反色处理提取轮廓
            cv2.bitwise_not(th, th)
            roi_A = th[200:240,0:320]
            roi_B = th[100:140,0:320]
            roi_C = th[20:60,0:320]
            
            #寻找颜色块
            try:
                A_feature = searchColorBlocks(frame, roi_A, 20, 200)
                B_feature = searchColorBlocks(frame, roi_B, 20, 100)
                C_feature = searchColorBlocks(frame, roi_C, 20, 20)
            except TypeError:
                print 'ColorBlocks is lost'
                pass

            if A_feature[2]==1 and B_feature[2]==1 and C_feature[2]==1:
                center_pos_x = int((A_feature[0]*weight_list_F[0]+B_feature[0]*weight_list_F[1]+C_feature[0]*weight_list_F[2])/sum(weight_list_F))
                center_pos_y = int((A_feature[1]*weight_list_F[2]+B_feature[1]*weight_list_F[1]+C_feature[1]*weight_list_F[0])/sum(weight_list_F))
                
            elif A_feature[2]==1 and B_feature[2]==1 and C_feature[2]==0:

                
                center_pos_x = int((A_feature[0]*weight_list_N[0]+B_feature[0]*weight_list_N[1])/sum(weight_list_N))
                center_pos_y = int((A_feature[1]*weight_list_N[1]+B_feature[1]*weight_list_N[0])/sum(weight_list_N))
                
            elif A_feature[2]==1 and B_feature[2]==0 and C_feature[2]==0:
                if A_feature[0] >= 170:
                    print 'right'
                elif A_feature[0] <= 140:
                    print 'left'
                else:
                    print 'forward'
            else:
                print 'stop'
                
            deflection_angle = -math.atan((center_pos_x-160)/(240.0-center_pos_y))
            
            deflection_angle = math.degrees(deflection_angle)
            print deflection_angle
            if s_flag == 1 :
                #PIDControl.motor_control(deflection_angle)   
                s_flag = 0
                print 'time set success'
            cv2.circle(frame,(center_pos_x,center_pos_y),5,(255,0,0),2)
        
            
            #显示
            cv2.imshow('video',frame)
            cv2.imshow('roia',roi_A)
            cv2.imshow('roib',roi_B)
            cv2.imshow('roic',roi_C)
            if cv2.waitKey(1) == 27:
                break
        '''
        Run.pwm_ENA1.stop()
        Run.pwm_ENA2.stop()
        Run.pwm_ENB1.stop()
        Run.pwm_ENB2.stop()
        Run.GPIO.cleanup()
        '''
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

        
