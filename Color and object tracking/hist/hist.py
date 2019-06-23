#-*- encoding:utf-8 -*-
# @author: zdl
# 绘制图像直方图

import cv2
import numpy as np
from scipy.misc import imresize
from matplotlib import pyplot as plt

img = cv2.imread('tankCar.jpg',1)
img = imresize(img, (240,320))

color = ('b', 'g', 'r')

for i, col in enumerate(color):
    hist = cv2.calcHist([img],[i],None,[256],[0,256])
    hist_max = np.where(hist == np.max(hist)) # 获取直方图最大的值及其索引
    print hist_max[0]
    plt.plot(hist, color = col)
    plt.xlim([0,256])

cv2.imshow('image', img)

# pyplot 绘图
 
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
