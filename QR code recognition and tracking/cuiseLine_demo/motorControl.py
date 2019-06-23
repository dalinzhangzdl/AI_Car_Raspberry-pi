#_*_ coding:UTF-8 _*_
# @author: zdl 
# FUNC: motor_control
# 电机PID控制，无舵机小车，差速转弯PID控制

# 导入PID函数及运动控制函数
import PID
import AICarRun as Run

# 设置全局速度，电机不同需做调整
mid = 80

# 程序运行次数统计
def counter(last=[1]):
    next = last[0]+1
    last[0] = next
    return next

# 电机PID控制
def motor_control(deflection_angle):
 
    global angle
    #count = counter()
    #print count
    angle = deflection_angle
    
    # PID参数初始化，设置Kp,Ki，Kd及控制量
    pid = PID.Incremental_PID(1.25, 0.0, 0.025)
    pid.setPoint = 0.0

    if abs(angle) <= 2.0:
        angle = 0.0
    
    # PID 计算
    pid.PID_compute(angle)
    output = pid.output
    print ('output', output)
    
    if output >= 50:
        output = 50
    elif output < -50:
        output = -50
    #output = output*1.5
    #output = output #(-30 30)
    r_duty = int(mid + output)
    l_duty = int(mid - output)
   
    # 速度上下限设置，不同电机需调整
    if r_duty < 50:
        r_duty = 50
    if l_duty < 50:
        l_duty = 50
    if r_duty >= 95:
        r_duty = 95
    if l_duty >= 95:
        l_duty = 95
    if r_duty - l_duty >35:
        r_duty = 95
        l_duty = 0
    elif l_duty -r_duty >35:
        r_duty = 0
        l_duty = 95
    print r_duty
    print l_duty
    
    # 电机PWM控制
    Run.forward(r_duty,l_duty)
    


