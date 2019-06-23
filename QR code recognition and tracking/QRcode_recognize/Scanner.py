#-*- coding: UTF-8 -*-   
# Simple QR code recognition
# @author: zdl

# import the necessary packages
#import simple_barcode_detection
import cv2
import numpy as np
import zbar
from PIL import Image

# create a reader
scanner = zbar.ImageScanner()
# configure the reader
scanner.parse_config('enable')
font=cv2.FONT_HERSHEY_SIMPLEX
camera=cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    grabbed, frame = camera.read()
    if not grabbed:
        break
    pil= Image.fromarray(frame).convert('L') # 转成灰度图像
    width, height = pil.size
    raw = pil.tobytes()
    zarimage = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(zarimage)
    for symbol in zarimage:  
    # do something useful with results 
        if not symbol.count: 
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data 
        cv2.putText(frame,symbol.data,(20,100),font,1,(0,255,0),4)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
