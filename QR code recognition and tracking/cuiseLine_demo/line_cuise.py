#_*_ coding:UTF-8 _*_
# @author: zdl 
# 图像ROI操作实现巡线功能

import cv2
import numpy as np
import math
import threading   # 导入多线程threading模块
import motorControl as PIDControl
import AICarRun as Run

# 定时器 修改para实现定时不同时间
def time_interrupt():
    global timer
    global s_flag
    s_flag = 1
    timer = threading.Timer(0.01,time_interrupt)
    timer.start() 

# 画白色十字光标
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
			 
# 寻找颜色块，并绘制直边界矩形
def searchColorBlocks(img, roi, hsv_lower, hsv_upper, Xoffset, Yoffset):
    
    # 图片掩膜和形态学操作
    mask = cv2.inRange(roi,hsv_lower,hsv_upper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
	
    # 寻找轮廓
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #print(len(cnts))
    # 获取外接矩形并绘制
    if len(cnts)>0:
        cnt = max(cnts, key = cv2.contourArea) # 寻找面积最大的轮廓
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(img,(x+Xoffset,y+Yoffset),(x+w+Xoffset,y+h+Yoffset),(255,0,0),2)
        drawCross(img,x+w/2+Xoffset,y+Yoffset+h/2,20)
        return (x+w/2+Xoffset,y+Yoffset+h/2) 
    else:
        print "not find"
    # return mid point
    

def main():
    global s_flag
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,46])
    weight_list = [0.3, 0.7]
    cap = cv2.VideoCapture(0)
    Run.motor_init()
    time_interrupt()
    if not cap.isOpened():
        print "camera is error, Please check"
    else:
	# 修改分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        while True:
            ret,frame = cap.read()
            
	    # 图像滤波、二值化及颜色空间转换 对于黑色线可以直接二值化处理不需要颜色空间转换处理
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            bgr = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
			
            # 图像ROI设定 选取上中下三块
            roi_A = hsv[200:240,20:300]
            roi_B = hsv[100:140,20:300]
            roi_C = hsv[20:60,20:300]
			
            #寻找颜色块
            try:
                Ax,Ay = searchColorBlocks(frame, roi_A, lower_black, upper_black, 20, 200)
                Bx,By = searchColorBlocks(frame, roi_B, lower_black, upper_black, 20, 100)
                Cx,Cy = searchColorBlocks(frame, roi_C, lower_black, upper_black, 20, 20)
            
                center_pos= int((Ax*weight_list[0]+Bx*weight_list[1]/sum(weight_list))) #+Cx*weight_list[2])/sum(weight_list))

		deflection_angle = -math.atan((center_pos-160)/120.0)
            
		deflection_angle = math.degrees(deflection_angle)
		print deflection_angle
		
            except TypeError:
                print 'ColorBlocks is lost'
                pass
            
            if s_flag == 1 :
                PIDControl.motor_control(deflection_angle)   
                s_flag = 0
                print 'time set success'
            cv2.circle(frame,(center_pos,120),5,(255,0,0),2)
        
            #显示
            cv2.imshow('video',frame)
            #cv2.imshow('roia',roi_A)
            #cv2.imshow('roib',roi_B)
            #cv2.imshow('roic',roi_C)
            if cv2.waitKey(1) == 27:
                break

        # release
        Run.gpio_release()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

        
