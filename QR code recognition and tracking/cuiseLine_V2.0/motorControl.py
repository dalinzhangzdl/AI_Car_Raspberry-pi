import threading
import time
import PID
import AICarRun as Run
import numpy as np

mid = 60

def counter(last=[1]):
    next = last[0]+1
    last[0] = next
    return next

def motor_control(deflection_angle):
    global time_list 
    global error_list 
    global angle
    #count = counter()
    #print count
    angle = deflection_angle
    pid = PID.Incremental_PID(1.25, 0.0, 0.025)
    pid.setPoint = 0.0

    if abs(angle) <= 3.0:
        angle = 0.0
    pid.PID_compute(angle)
    output = pid.output
    print ('output', output)
    
    if output > 50:
        output = 50
    elif output < -50:
        output = -50
    output = output*1.5
    output = output #(-30 30)
    r_duty = int(mid + output)
    l_duty = int(mid - output)+2
        #if abs(r_duty - l_duty) < 10:
        #   r_duty += 5
          #  l_duty += 5
    if r_duty < 40:
        r_duty = 40
    if l_duty < 40:
        l_duty = 40
    if r_duty >= 80:
        r_duty = 80
    if l_duty >= 80:
        l_duty = 80
    if r_duty - l_duty >20:
        r_duty = 80
        l_duty = 20
    elif l_duty -r_duty >20:
        r_duty = 20
        l_duty = 80
    print r_duty
    print l_duty
    Run.r_forward(r_duty,l_duty)
    


