#_*_ coding:UTF-8 _*_
'''
Class  : Incremental PID
Author : zdl
Date   : 2018/7/12
Fun    : Incremental PID controller

'''
import time

# class Incremental_PID inherit object 
class Incremental_PID(object): 
    ''' PID controller'''

    def __init__(self,P=0.0,I=0.0,D=0.0):
        self.setPoint = 0.0
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.last_error = 0.0
        self.P_error = 0.0
        self.I_error = 0.0
        self.D_error = 0.0
        #Anti-integration saturation parameter
        self.I_saturation = 10.0
        # PID out
        self.output = 0.0

    # PID Calculation
    def PID_compute(self,feedback_val):
        '''Incremental_PID
            math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        '''
        # compute PID_error
        error = self.setPoint - feedback_val
        self.P_error = self.Kp * error
        self.D_error = self.Kd * (error - self.last_error)
        self.I_error += error
        
        #抗积分饱和
        if (self.I_error < -self.I_saturation ):
            self.I_error = -self.I_saturation
        elif (self.I_error > self.I_saturation):
            self.I_error = self.I_saturation
			
	# PID output
        self.output = self.P_error + (self.Ki * self.I_error) + self.D_error
		
        self.last_error = error

    # set Kp
    def setKp(self,proportional_gain):
        self.Kp = proportional_gain

    # set Ki
    def setKi(self,integral_gain):
        self.Ki = integral_gain

    # set Kd
    def setKd(self,derivative_gain):
        self.Kd = derivative_gain
		
		
    # set integral saturation
    def setI_saturation(self,saturation_val):
        self.I_saturation = saturation_val

    
