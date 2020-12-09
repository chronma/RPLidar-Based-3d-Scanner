# by chris martin 9/9/2020
# Uses bits and pieces from the internet
# Python Script is for Python 3

from Stepper_Motor_Control_2 import motorcontrol  #motor class 
import time # maybe better to use Gevent. eventually
import subprocess #allows command line to be used in the program
import math #math and trig functions

pi=math.pi #pi constant

mc=motorcontrol() # mc stepper motor 
frequency=2000 #pwm frequency

m1=0
m2=0
if m2 == 0 and m1 == 0: #1/8 step
    multiplier=8
if m2==0 and m1 == 1: #1/2 step
    multiplier=32  
if m2==1 and m1 == 0: #1/4 step
    multiplier=64
if m2==1 and m1 == 1: #1/16 step
    multiplier=16

motorsteps=400 #steps full steps per rev
driveratio=128/16

Nstepsperrev=driveratio*motorsteps*multiplier # physical steps per rev 1.8 deg stepper motor drive ratio is 8*200*16 (3200*)
timeperrev=Nstepsperrev/frequency
zaxisindex=1 # number of scans to take on the zaxis
zaxisanglestep=pi/zaxisindex # only will be rotating 180deg

Nscancycles=4 # rplidar scan rotations

zaxisruntime=timeperrev/zaxisindex
#zaxisruntime=15
print ("runtime:", zaxisruntime)
mc.zaxis(1,1,frequency,m1,m2,50, zaxisruntime*.5) #lock zaxis duty=100
mc.zaxis(0,1,frequency,m1,m2,50, zaxisruntime/2) #lock zaxis duty=100