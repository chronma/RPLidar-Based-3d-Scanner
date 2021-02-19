# python 3
# by Chris Martin 12/6/2020
# Modified for Raspberry Pi by Tom Watts
# Uses a TMC2209 v3.0
# Enable TMC2209(pin 1) to RPi GPIO24 (pin 18), Direction TMC2209(pin8) to RPi GPIO23 (pin 16)
# M1 TMC2209(pin 2) to RPi GPIO7 (pin 26), M2 TMC2209(pin 3) to RPi GPIO25 (pin 22),M3 (8825 only) pin 4 to RPi GPIO 22 (pin 15)
# step TMC2209(pin 7) to RPi GPIO18 (pin 12)
# Import Modules
import time
import subprocess
import RPi.GPIO as GPIO
# motorcontrol class
class motorcontrol(object):
    # intitialize
    def __init__(self,
                 enable=24,
                 direct=23,
                 M1_port=7,
                 M2_port=25,
                 step=18):
      
        #zaxis
        self.enable = enable
        self.direct = direct
        self.M1_port = M1_port
        self.M2_port = M2_port
        self.step = step
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(step, GPIO.OUT)
        self.pwm = GPIO.PWM(step, 100)
        GPIO.setup(direct, GPIO.OUT) #direction
        GPIO.setup(enable, GPIO.OUT) #enable
        GPIO.setup(M1_port, GPIO.OUT) #M1
        GPIO.setup(M2_port, GPIO.OUT) #M2
        GPIO.setup(step, GPIO.OUT) #stepper
        print ("Stepper Motor initialized")
    # destructor
    def __del__(self):
        self.pwm.stop()
        GPIO.output(self.enable,1) #enable
        GPIO.cleanup()
        print ('end')

    def cutpower(self):
        self.pwm.stop()
        GPIO.output(self.enable,1) #set to one to disable
        GPIO.cleanup()
        print ('end')

    def zaxis(self,direction,active,frequency,m1,m2,duty,runtime):
        
        if active==1:
            GPIO.output(self.direct,direction) #direction
            GPIO.output(self.enable,0) #enable
            GPIO.output(self.M1_port,m1) #M1
            GPIO.output(self.M2_port,m2) #M2
            
        self.pwm.start(duty)  #run for time
        time.sleep(runtime) 
        self.pwm.stop()
        
        
    
            
            
        
