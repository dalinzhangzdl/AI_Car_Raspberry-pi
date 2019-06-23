# -*- coding: UTF-8 -*-
# motorControl.py python2.7
# @author: zdl
# func: 电机差速PID控制


import PID as PID
import AICarRun as Run
import math
import numpy as np

Width = 640

# 电机差速PID控制
def motor_control(point_x, point_y,mid_PWM):
    global time_list 
    global error_list 
    global angle

    if point_x > 0 and point_x < 640:
        pid = PID.Incremental_PID(1.05, 0.0, 0.02)
        pid.setPoint = 90.0
        if point_x > Width/2+5:
            angle = 90-math.degrees(math.atan(float(point_x-160)/float(240-point_y)))
        
        elif point_x < Width/2-5:
            angle = 90+math.degrees(math.atan(float(160-point_x)/float(240-point_y)))
        
        else:
            angle = 90.0

        pid.PID_compute(angle)
        output = pid.output
    
        print ('output', output)
        if output > 90:
            output = 90
        elif output < -90:
            output = -90  
        output = output/1.2#(-30 30)
        if abs(output) < 1.0:
            output = 0

        # AI car motor2.0
        if mid_PWM!= 0:
            r_duty = int(mid_PWM + output)
            l_duty = int(mid_PWM - output)
            
            if r_duty < 55:
                r_duty = 55
            if l_duty < 55:
                l_duty = 55
            if r_duty >= 100:
                r_duty = 100
            if l_duty >= 100:
                l_duty = 100
            if r_duty - l_duty > 30:
                r_duty = 72
                l_duty = 0
            elif l_duty - r_duty > 30:
                r_duty = 0
                l_duty = 72
        else:
            if abs(output) < 3:
                r_duty = 0
                l_duty = 0
            else:
                if output >8:
                    output = 8
                if output <-8:
                    output = -8
                r_duty = int(output*10 )
                l_duty = int(-output*10)
    else:
        r_duty = 0
        l_duty = 0
    print r_duty
    print l_duty
    Run.forward(r_duty,l_duty)


