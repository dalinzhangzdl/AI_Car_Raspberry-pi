#-*- encoding:utf-8 -*-
# @author: zdl
# 绘制HSV颜色空间2D直方图

import cv2
import numpy as np
from scipy.misc import imresize
from matplotlib import pyplot as plt

img = cv2.imread('tankCar.jpg',cv2.IMREAD_COLOR)
img = imresize(img, (240,320))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 生成2D直方图
hist = cv2.calcHist([hsv],[0, 1],None,[180, 256],[0, 180, 0, 256])

cv2.imshow('image', img)

# pyplot 绘图
plt.imshow(hist, interpolation = 'nearest') 
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
