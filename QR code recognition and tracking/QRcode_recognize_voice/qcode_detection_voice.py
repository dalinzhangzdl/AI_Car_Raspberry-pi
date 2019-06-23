# -*- coding: UTF-8 -*-
# Simple QR code detection
# @author: zdl
# func: 识别二维码并语音合成播报其内容

import cv2
import numpy as np
import zbar
import tts
import os 

# 二维码定位
def find_code(img):
    
    # 滤波
    blur = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # 形态学操作
    mask=cv2.erode(th,None,iterations=4)
    mask=cv2.dilate(mask,None,iterations=4)
    cv2.bitwise_not(mask, mask)

    # 寻找轮廓
    _,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)>0:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 500:
            print cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)

            try:
                img = cv2.rectangle(img,(x-15,y-15),(x+w+15,y+h+15),(0,255,0),3)

                img_ROI = img[y-15:y+h+15, x-15:x+w+15]
            except:
                img = cv2.rectangle(img,(x, y),(x+w, y+h),(0,255,0),3)
                img_ROI = img[y:y+h, x:x+w]
        
        else:
            img_ROI = img
    else:
        img_ROI = img

    return img_ROI


if __name__ == '__main__':

    img = cv2.imread('yahboom.jpg', 1)

    # 二维码定位
    img_ROI = find_code(img)

    # zbar 初始化
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    img_ROI_gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
    width, height = img_ROI_gray.shape
    raw = img_ROI_gray.tobytes()

    # 扫码及解码
    zarimage = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(zarimage)
    for symbol in zarimage:  
    # do something useful with results 
        if not symbol.count:
            string = symbol.data
            tts.tts(string)
            print 'decoded', symbol.type, 'symbol', '"%s"' % string
            os.system('mplayer %s' % 'synthesis.mp3')
        else:
            print 'no'
        #cv2.putText(img,symbol.data,(20,100),font,1,(0,255,0),4)
    
    cv2.imshow('img_ROI', img_ROI_gray)
    cv2.imshow('image', img)
    cv2.waitKey(0)
                

    
