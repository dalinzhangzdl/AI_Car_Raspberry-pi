#-*- encoding:utf-8 -*-
# @author: zdl
# 使用openCV实现截图
# 按下空格键实现截图，截图文件保存在设置的文件夹下

import cv2
import numpy as np 

# 保存路径设置
savepath = './shootimage/'  # 需自行在程序文件夹下新建文件夹或指定相对文件路径
shot_idx = 0

# 摄像头设置
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while(cap.isOpened()):
    ret,frame = cap.read()
    cv2.imshow('image',frame)
	
    #获取键盘按键值，按下空格键实现截图
    ch = cv2.waitKey(1)
    if ch == ord(' '):
        fn = savepath+str(shot_idx)+'.jpg'
        cv2.imwrite(fn,frame)
        print (fn, 'saved')
        shot_idx +=1
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
        

    
