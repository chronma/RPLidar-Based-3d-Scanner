    #import the library
import spidev
import Adafruit_BBIO.GPIO as GPIO     
import time
from scanner_support_functions import anglesensor
import subprocess
from Stepper_Motor_Control_2 import motorcontrol  #motor class 


spi = anglesensor(0,0,1)
mc=motorcontrol() # mc stepper motor 
frequency=500 #pwm frequency
m1=0
m2=0

ave=0
vmax=361.0
vmin=0.0
count=0
rollover=0
oneshot=False
driveratio=8
flag=0
while count<1000:
    angle=spi.getangle()
    
    if not oneshot:
        startangle=angle
        lastangle=angle
        startangleprime=360-startangle
        oneshot=True
    if lastangle<angle and angle>300 and lastangle<40 and flag==0:
        rollover +=1
        flag=1
    if flag ==1 and angle<320.0 and angle>40: flag=0    
        
    
    angleprime=360-angle
    posangle=(angleprime-startangleprime+360*rollover)/driveratio
    print('{:12.4f}'.format(lastangle), '  {:12.4f}'.format(angle),'rollover: ', rollover,'pos  {:12.4f}'.format(posangle),  'pos  {:12.4f}'.format(angle-lastangle), end='\r')
    #print('angle: ',(angle), end='\r')
    mc.zaxis(0,1,frequency,m1,m2,50, 0.03) #lock zaxis duty=100
    time.sleep(.001)
    count +=1
    
    lastangle=angle
    
spi.close()

