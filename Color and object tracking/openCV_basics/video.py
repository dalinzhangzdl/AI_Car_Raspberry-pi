#-*-coding:UTF-8 -*-
# @author: zdl
'''
视频读取、显示和保存综合实验。
按下ESC键退出程序
'''

import cv2

cap = cv2.VideoCapture(0)
#设置视频输出
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while (cap.isOpened()):    #摄像头是否正常开启
    ret, frame = cap.read()
    out.write(frame)      # 写视频
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 27 :
        break
    
# 释放资源   
cap.release()
out.release() 
print '视频保存成功'
cv2.destroyAllWindows()  #关闭窗口
