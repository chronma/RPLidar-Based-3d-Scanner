# python 3
#motor control
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import subprocess

# NOTES

# variable to set frequency and pulse width for testing
        #freq = 500 #Hz
        #duty = 50 #%
        #PWM.start("P8_34",duty,freq,0)  #PWM1A pin P8-36
        #PWM.start("P9_31",duty,freq,0)  #PWM1A pin P8-36
        # need to set pin to pwm # config-pin -a p9.31 pwm 
        #PWM.start("P8_45",duty,freq,0)  #PWM2A pin P8-45
        # need to set pin to pwm # config-pin -a p8.45 pwm 


class motorcontrol(object):
    #globals for testing
    
    # intitialize
    def __init__(self):
        
        # line runs bash command to config pin, if the cape manager is not loaded it will be triggered to load doesnt matter what pin is set
        #subprocess.check_call("config-pin -a p9.14 pwm",shell=True)
        
        # Stepper Motor Control 1 & 2 (Camera arm spin and z axis)
        # set up pins to run stepper motor pulse & direction
        
        #zaxis
        
        GPIO.setup("P9_15", GPIO.OUT) #direction
        GPIO.setup("P9_13", GPIO.OUT) #enable
        GPIO.setup("P9_23", GPIO.OUT) #M1
        GPIO.setup("P9_25", GPIO.OUT) #M2
        print ("initilized")
    # destructor
    def __del__(self):
        
        #zxis
        PWM.stop("P9_16")
        GPIO.output("P9_15",0) #direction
        GPIO.output("P9_13",1) #enable
        GPIO.output("P9_23",0) #M1
        GPIO.output("P9_25",0) #M2
       
        
        PWM.cleanup()
        print ('end')

    def cutpower(self):
        
        #zxis
        PWM.stop("P9_16")
        GPIO.output("P9_15",0) #direction
        GPIO.output("P9_13",1) #enable
        GPIO.output("P9_23",0) #M1
        GPIO.output("P9_25",0) #M2
        
        print ('end')
        PWM.cleanup()

    def zaxis(self,direction,active,frequency,m1,m2,duty,runtime):
        
        if active==1:
            GPIO.output("P9_15",direction) #direction
            GPIO.output("P9_13",0) #enable
            GPIO.output("P9_23",m1) #M1
            GPIO.output("P9_25",m2) #M2
            
        
        PWM.start('P9_16',duty,frequency,0)  #run for time
        time.sleep(runtime) 
        #PWM.start('P9_16',0,frequency,0)   #stop and lock pos
        PWM.stop('P9_16')
        
        
    
            
            
        