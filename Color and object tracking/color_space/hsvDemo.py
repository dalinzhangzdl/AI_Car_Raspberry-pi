#-*-coding:UTF-8 -*-
# @author: zdl
'''
颜色空间变换实验
BGR颜色空间转换为HSV颜色空间，构建掩膜实现颜色识别
实现红色和黄色块的识别
HSV值的范围  H[0,179]  S[0,255]  V[0,255]
'''

import numpy as np
import cv2

# 创建图片和颜色块
img = np.ones((240,320,3),dtype = np.uint8)*255
img[100:140, 140:180] = [0,0,255]
img[60:100,60:100] = [0,255,255]
img[60:100,220:260] = [255,0,0]
img[140:180,60:100] = [255,0,0]
img[140:180,220:260] = [0,255,255]

# 设定红色的HSV值
yellow_lower = np.array([26,43,46])
yellow_upper = np.array([34,255,255])
red_lower = np.array([0,43,46])
red_upper = np.array([10,255,255])

# 颜色空间变换 BGR—>HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 构建掩膜
mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
mask_red = cv2.inRange(hsv, red_lower, red_upper)

# 利用掩膜位运算
mask = cv2.bitwise_or(mask_yellow,mask_red) # 或运算
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('image', img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
