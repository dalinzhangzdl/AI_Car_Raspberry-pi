#-*-coding:UTF-8 -*-
# @author: zdl
'''
使用OpenCV函数绘制常用图形
在一幅图片上画线，画圆，画矩形和文字。
'''

import cv2
import numpy as np

img = np.zeros((512,512,3), dtype=np.uint8)        #创建一幅图像

cv2.line(img,(0,0),(500,500),(255,0,0),5)          #绘制直线
cv2.circle(img,(255,255),50,(0,255,0),-1)          #绘制填充圆
cv2.circle(img,(255,255),80,(255,255,0),5)         #绘制非填充圆
cv2.rectangle(img,(170,170),(340,340),(0,0,255),2) #绘制矩形

# 绘制文本
cv2.putText(img,'Learn OpenCV',(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
cv2.putText(img,'Yahboom Technology',(70,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)

cv2.imshow('image', img)    #显示图像

#等待释放窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
