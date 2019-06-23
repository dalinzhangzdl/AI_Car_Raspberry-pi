#-*-coding:UTF-8 -*-
# @author: zdl
'''
颜色追踪实验
BGR颜色空间转换为HSV颜色空间，构建掩膜实现颜色识别
寻找掩膜运算过的图片的轮廓，轮廓面积最大的区域就是要追踪的物体
HSV值的范围  H[0,179]  S[0,255]  V[0,255]
按键按下ESC退出程序
'''
# 导入包
import numpy as np
import cv2

# 设定追踪物体颜色阈值  蓝色
blue_lower = np.array([100,50,50])
blue_upper = np.array([124,255,255])
cap=cv2.VideoCapture(0)

# 修改摄像头的分辩率  320*240
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame,(5,5),0)  # 高斯滤波
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 颜色空间变换
	mask = cv2.inRange(blue_lower,blue_upper)     # 根据阈值构建掩模
	
	# 图像形态学操作，膨胀腐蚀
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)
    mask = cv2.GaussianBlur(mask,(3,3),0)
    
    res = cv2.bitwise_and(frame,frame,mask=mask)  # 对源图像进行位操作
	# 寻找轮廓，并绘制轮廓
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
							cv2.CHAIN_APPROX_SIMPLE)[-2]   
    if len(cnts) > 0:
		# 寻找面积最大的轮廓并画出其最小外接圆
        cnt = max(cnts, key=cv2.contourArea )        
        (x,y), radius = cv2.minEnclosingCircle(cnt)  
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2)  
        print(int(x),int(y))    # 打印追踪物体的中心坐标
    else:
        pass
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    if cv2.waitKey(5)&0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
