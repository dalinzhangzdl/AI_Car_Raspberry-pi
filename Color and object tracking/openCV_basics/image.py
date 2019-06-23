#-*-coding:UTF-8 -*-
# @author: zdl
'''
图像读取、显示和保存综合实验。
按下ESC键退出程序，按下s键保存图片
'''
import cv2

img = cv2.imread('tankCar.jpg',cv2.IMREAD_COLOR)  #读取图像

cv2.imshow('image',img)         #显示图像

k = cv2.waitKey(0)              #获取键盘按下的键值
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('car.jpg', img)
    print '保存图片成功'
    cv2.destroyAllWindows()
