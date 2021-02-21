# python 3
#motor control
#import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.PWM as PWM
import RPi.GPIO as GPIO
import time
import subprocess
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ENABLE = 24 #2209 motor driver enable (active low)
DIR = 23    #2209 motor driver direction
M1_port = 7      #2209 microstep resolution
M2_port = 25     #2209 Microstep resolution
STEP = 18   #2209 PWM steps pin
# Setup outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT) #direction, zero is clockwise, 1 is anticlockwise
GPIO.setup(ENABLE, GPIO.OUT) #enable
GPIO.setup(M1_port, GPIO.OUT) #M1
GPIO.setup(M2_port, GPIO.OUT) #M2
GPIO.setup(STEP, GPIO.OUT)# the step port
# setup pins
GPIO.output(DIR,0) #direction
GPIO.output(ENABLE,0) #set to one to disable and zero to enable
GPIO.output(M1_port,0) #M1
GPIO.output(M2_port,0) #M2
def stepper(direction, m1, m2, step_number, delay):
    if m2 == 0 and m1 == 0: #1/8 step
        multiplier=8
    if m2==0 and m1 == 1: #1/2 step
        multiplier=32  
    if m2==1 and m1 == 0: #1/4 step
        multiplier=64
    if m2==1 and m1 == 1: #1/16 step
        multiplier=16
    GPIO.output(ENABLE,0) #set to zero to enable
    GPIO.output(DIR,direction)
    time.sleep(delay)
    for n in range(0, step_number * multiplier):
        GPIO.output(STEP,0)
        time.sleep(delay)
        GPIO.output(STEP,1)
        time.sleep(delay)
    return

# Main program
try:
    angle = 18.0
    anglenow = 0
    while anglenow < 360:
        stepper(0, 0, 1, 20, 0.0004)
        anglenow+= angle
        print("angle is:- ", anglenow) 

    while anglenow > 1:
        stepper(1, 0, 1, 20, 0.0004)
        anglenow-= angle
        print("angle is:- ", anglenow) 

    GPIO.cleanup()    
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
        
        
    
            
            
        
