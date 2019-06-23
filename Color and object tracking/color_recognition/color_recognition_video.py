#_*_ coding:UTF-8 _*_
# @author: zdl 
# 统计HSV颜色空间H的直方图，实现实时视频物体的颜色识别

import cv2
import numpy as np
#from matplotlib import pyplot as plt

# 计算统计颜色直方图
def color_hist(img):
    #构建掩膜
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[70:170,100:220] = 255
    
    #生成HSV颜色空间 H 的直方图
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], mask, [180], [0, 180])
    
    #统计直方图识别颜色
    object_H = np.where(hist_mask==np.max(hist_mask)) # 获取直方图最大的值及其索引
    print object_H[0]
    return object_H[0]
    
    #plt.plot(hist_mask)
    #plt.xlim([0,180])
    #plt.imshow(hist,interpolation = 'nearest')
    #plt.show()

# 判断直方图H的值，实现颜色识别
# yellow (22,36) red(156,180) blue(100,124),green(35,77) cyan-blue(78,99)orange(6,20)
# try except 捕获object_H存在多个值的异常
def color_distinguish(object_H):
    try:
        if object_H > 26 and object_H < 34:
            color = 'yellow'
        elif object_H > 156 and object_H < 180:
            color = 'red'
        elif object_H > 100 and object_H < 124:
            color = 'blue'
        elif object_H > 35 and object_H < 77:
            color = 'green'
        elif object_H > 78 and object_H < 99:
            color = 'cyan-blue'
        elif object_H > 6 and object_H < 15:
            color = 'orange'
        else:
            color = 'None'
        print color
        return color
    except:
        pass

# mian()函数      
if __name__ == '__main__':

    time_delay = 0  # 延时变量
	
    # 打开摄像头并修改分辨率
    cap = cv2.VideoCapture(0)
    if cap.isOpened() == 0:
        print 'camera is error, Please check!'
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    while(cap.isOpened()):
	# 获取视频流，定时识别物体颜色
        ret, frame = cap.read()
        time_delay +=1
        if time_delay >= 10:
            object_H = color_hist(frame)
            color_distinguish(object_H)
            time_delay = 0
        cv2.rectangle(frame,(100,70),(220,170),(0,255,0),2)	
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:    # ESC退出程序
            break
	
    cap.release()
    cv2.destroyAllWindows()
    
