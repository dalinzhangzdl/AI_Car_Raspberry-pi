#-*-coding:UTF-8 -*-
# @author: zdl
'''
创建滑动条实验
获取三个RGB三个滑动条的值，实现调色板功能
按键按下ESC退出程序
'''
import cv2
import numpy as np

# create empty callback
def nothing(x):
    pass

# 创建一幅黑色图片
img = np.zeros((320,512,3), dtype=np.uint8)
#创建一个窗口
cv2.namedWindow('image')

#创建滑动条
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

while True:
    cv2.imshow('image',img)
	
    #获取滑动条的值
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
	# 将BGR的值赋给图像矩阵
    img[:] = [b,g,r]
    if cv2.waitKey(1)&0xFF == 27:
        break
cv2.destroyAllWindows()


