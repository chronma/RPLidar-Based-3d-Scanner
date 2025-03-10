# by chris martin 2/11/2025
# Uses bits and pieces from the internet
# Python Script is for Python 3

from pru_SMC import motorcontrol  #motor class 
import time # maybe better to use Gevent. eventually
import subprocess #allows command line to be used in the program
import math #math and trig functions
import ctypes
from ctypes import *

pi=math.pi #pi constant

mc=motorcontrol() # mc stepper motor 
    
command_bits=0
m1=1
m2=1
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

Nscancycles=4 # rplidar scan rotations

#zaxisruntime=timeperrev/zaxisindex
zaxisangle= (360*1)  #deg
zaxisspeed=30 #degree/sec
zacceltime=0
#command_bits=mc.zaxis(command_bits,zaxisangle,zaxisspeed,zacceltime,m1,m2,multiplier) #
command_bits=mc.zaxis(command_bits,-zaxisangle,zaxisspeed,zacceltime,m1,m2,multiplier) #

