# -*- coding: UTF-8 -*-   
# QR_navigation.py python2.7
# @author: zdl
# func: 识别二维码控制AI车的运动，实现导航。


import cv2
import numpy as np
import zbar
from PIL import Image
import AICarRun as Run


# car state
enStop = 0
enRun = 1
enBack = 2
enLeft = 3
enRight = 4
car_State = 0
symbolPos = []
last_qr_data = 'no qrcode'
global qr_data

def draw_rect(img, pos, color, width):
    cv2.line(img, pos[0], pos[1], color, width)
    cv2.line(img, pos[0], pos[3], color, width)
    cv2.line(img, pos[2], pos[1], color, width)
    cv2.line(img, pos[2], pos[3], color, width)

def qr_scan_decode(img):
    global qr_data
    
    pil= Image.fromarray(img).convert('L')  # gray
    width, height = pil.size
    raw = pil.tobytes()
    zarimage = zbar.Image(width, height, 'Y800', raw)
    scanner_Flag = scanner.scan(zarimage)
    if scanner_Flag == 1:
        for symbol in zarimage:
            if not symbol.count:
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                symbolPos = symbol.location
                draw_rect(img, symbolPos, (0,255,0), 3)
                qr_data = str(symbol.data)
            else:
                qr_data = 'no qrcode'
    else:
        qr_data = 'no qrcode'
    if last_qr_data != qr_data:       
        command_resolve(qr_data)
    last_qr_data = qr_data

def command_resolve(command):
    last_car_state = 0
    if command.find("Run",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 1
    elif command.find("Back",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 2
    elif command.find("Left",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 3
    elif command.find("Right",0,len(command)) != -1:
        command.zfill(len(command))
        car_state = 4
    elif command.find("Stop",0,len(command)) != -1:            
        command.zfill(len(command))
        car_state = 0
    else:
        car_state = 5
        command.zfill(len(command))
    #print car_state
   
    if last_car_state != car_state :
        car_control(car_state)
    last_car_state = car_state
def car_control(car_state):
    
    if car_state == enRun:
        Run.run(1)
    elif car_state == enBack :
        Run.back(2)
    elif car_state == enLeft :
        Run.left(2)
    elif car_state == enRight :
        Run.right(2)
    elif car_state == enStop:
        Run.brake(0)
    else:
        Run.brake(0)

if __name__ == '__main__':

    Run.motor_init()
    # create a reader
    scanner = zbar.ImageScanner()
    # configure the reader
    scanner.parse_config('enable')
    font = cv2.FONT_HERSHEY_SIMPLEX
    # set camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened()==0 :
        print("camera iserror")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while(True):
        grabbed, frame = cap.read()
        if not grabbed:
            break
        qr_scan_decode(frame)
    
    #cv2.putText(frame,symbol.data,(20,100),font,1,(0,255,0),4)
    #print car_state

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27: # ESC key break
            break
# release camera and GPIO
    Run.release()
    cap.release()
    cv2.destroyAllWindows()
