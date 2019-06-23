#-*-coding:UTF-8 -*-
# @author: zdl
'''
加载OpenCV官方自带的级联分类器实现人脸识别
实现人脸和人眼识别
'''
import numpy as np
import cv2

#加载人脸识别和人眼识别分类器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_cascade.load('‪D:/Zdl_Data/python-opencv/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#eye_cascade.load('D:/Zdl_Data/python-opencv/haarcascade_eye.xml')

img = cv2.imread('luxun.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#人脸识别
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
print ('发现了{0}个人脸'.format(len(faces)))
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
	
	# 人眼识别
    eyes = eye_cascade.detectMultiScale(roi_gray)
    print ('发现了{0}个眼睛'.format(len(eyes)))
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
