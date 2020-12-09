# by chris martin 12/6/2020
# Uses bits and pieces from the internet
# Python Script is for Python 3

# running the pylidaylibtest.py script a couple of times can reset the link to the rplidarmodule in the event the com link is left open
# ex. the script is aborted early.
# running the z axis test loop can help the stepper driver self tune (TMC2209) the 8825 drivers dont need this.

import select # Not sure what features this library all has
import time # maybe better to use Gevent. eventually
import subprocess #allows command line to be used in the program
import math #math and trig functions
import scanner_support_functions
from Stepper_Motor_Control_2 import motorcontrol  #motor class
from scanner_support_functions import anglesensor #zaxis feed back
from pyrplidar import PyRPlidar #python rplidar library from https://github.com/Hyun-je (modified slightly for this application)

#CONSTANTS / initialize
pi=math.pi #pi constant
intensity="150" #strength of the laser return, turns out this is only availible if the scanner is in legacy mode.
loopend=0 #initialize looping variable
zaxisangle=0 #initialize zaxis angle 

first=0
counter_scan_loops=-5

#SET UP Z-AXIS
mc=motorcontrol() # mc stepper motor 
frequency=1000 #pwm frequency
direction=0 # Scanner operates clockwise viewed from top
m1=0 # Legacy mode stepper driver step selection
m2=1 # Legacy mode stepper driver step selection
motorsteps=400 #steps full steps per rev
driveratio=128/16 #driven 128th/ drive 16th
spi = anglesensor(0,0,1) #angle sensor on spi 0,0 mode 1
oneshot=False  
flag=0
rollover=0
calczaxisangle=0

#RUNTIME VARIBLES
zaxisindex=8000 # number of scans to take on the zaxis tested up to 6000 so far with angle sensor
Nscancycles=2 # rplidar scan rotations the rplidar module does nto always give the same angles for measurements, a higher number here
                                                # results in more points collected 10 times around gives a high density of points but take longer
distancelimit=4500 # throw away points that are too far out.
RPLIDARanglecorrection=0.01745329*1.00 #.98  #1 DEG*FACTOR - the rplidar x axis "0 degrees"  this horizontal this adgusts the plane. 
zaxiscorrection = math.radians(0.0)#

#SET UP Z AXIS STEP SIZE AND STEPPER MOTOR RUN TIME (NO ANGLE SENSOR)
zaxisanglestep=2*pi/zaxisindex  # 360degrees divided by how many steps to take
zaxisruntime=scanner_support_functions.getzaxisruntime(frequency,motorsteps,driveratio,m1,m2,zaxisindex,Nscancycles)
timeperrev=zaxisruntime*zaxisindex # this is used to bring the scanner back home after scannning will use it to tune the stepper driver too 

# SET UP RPLIDAR
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=5)  #USB also can set up uart pins if desired
lidar.set_motor_pwm(1000) # not needed for RPLIDAR A1 AS YOU CAN'T CHANGE THE SPEED.
scan_generator = lidar.start_scan_express(0,"raw") # raw if using typed data from scanner, not raw for data packed in string
#0,1,2 is the scan type 0 is the express scan it gives 4000 measurements around generally the slower the better the accuracy appears to be
time.sleep(2) # wait for rplidar to finish set up

#open file for writing scan points as ascii
filename=scanner_support_functions.getfilename()
rootname="_points_a.xyz"
f = open(filename+rootname, 'a') #open point file for appending scan points xyz ascii data
rootname="_points_b.xyz"
g = open(filename+rootname, 'a') #open point file for appending scan points xyz ascii data
#scanning routine
counter_scan_loops=0
# scan loop

for count, scan in enumerate(scan_generator()): # this takes the scan data and adds a count to the start of each measurement
        if scan[0]==True: # gives true a the start of each full revolution measured.
            counter_scan_loops = counter_scan_loops + 1
        if counter_scan_loops == 4: 
            break #"warm up scanner give it a chance to stabilize"
counter_scan_loops=0
while not loopend:
    
    rawangle=spi.getangle()  #get stepper motor angle
    
    if not oneshot:  #zero out steppper motor angle
        startangle=rawangle
        lastangle=rawangle
        startangleprime=360-startangle
        
    if lastangle<rawangle and rawangle>300 and lastangle<40 and flag==0: #stepper turns 8 times for every time the scanner turns once 
        rollover +=1
        flag=1
    if flag ==1 and rawangle<320.0 and rawangle>40: flag=0    
    angleprime=360-rawangle
    
    posangle=(angleprime-startangleprime+360*rollover)/driveratio  #calculate zaxis angle
    lastangle=rawangle
    if not oneshot:
        startposangle=posangle
        oneshot=True
    
    
    zaxisangle=math.radians(posangle) # convert to radians
    
    lidar.clear_buffer() #the scanner is scanning all the time, this forces it erase anything in its memory and start sending data agfain from 0 degrees
    time.sleep(.005) #timer to clear buffer seems to work fine with out the wait maybe not needed.
    
    for count, scan in enumerate(scan_generator()): # this takes the scan data and adds a count to the start of each measurement
        if scan[0]==True: # gives true a the start of each full revolution measured.
            counter_scan_loops = counter_scan_loops + 1
        
        distance=scan[3] #measured distance
        angle=math.radians(scan[2])+RPLIDARanglecorrection #measured angle realtive to horizontal corrected for error in mounting
        cosalpha=math.cos(angle) # cosine
        sinalpha=math.sin(angle) # sine
        costheta=math.cos(zaxisangle) # cosine zaxis rotation
        sintheta=math.sin(zaxisangle) # cosine zaxis rotation
             
        # rotate about y axis first y stays constant
        xprime=(distance*cosalpha)
        zprime=(-distance*sinalpha)
        yprime=0
           
        #rotate about z axis second z stays constant
        x=1*(xprime*costheta)
        y=-1*(xprime*sintheta)
        z=(zprime)
        if scan[1]>0 and scan[3]<distancelimit: # check scan quality for 0 (bad measure) and that it is in range
            if scan[1]>255: intensity='150' # keep intesity in range (doesnt do anything, just in case)
            #else: intensity=255-int((scan[3]/distancelimit)*255)  # set intensity to be based on distance (could color code it)
            
            if angle <=pi/2 or angle >= 3*pi/2:
                print (str(x),str(y),str(z),intensity,intensity,intensity, '\n', file=f) # print data to file.
            else:
                print (str(x),str(y),str(z),intensity,intensity,intensity, '\n', file=g) # print data to file.
            # there appears to be some paralax in the rplidar sensing. plan was to scan 180 deg on the z axis to get 360 deg coverage
            #, but the seams would not reconcile. the error appears to be the width of the laser dot so to speak 
            # so now it creates two point cloud files using the front and back scanned hemisphere
        
        if counter_scan_loops == (Nscancycles+1): 
            print("count:", (str(count)).zfill(5),end=' ')
            break
    counter_scan_loops=0 # rest counter for scan looops
    
    print ("calculated angle: ",'{:12.4f}'.format(math.degrees(calczaxisangle))," measured angle:",'{:12.4f}'.format(posangle), end='\r')       
    
    calczaxisangle=calczaxisangle+zaxisanglestep #count up zaxis revolutions
    
     
    if zaxisangle > (startposangle+(2*pi)):
        loopend=1
    mc.zaxis(direction,1,frequency,m1,m2,50, zaxisruntime) #lock zaxis duty=100)
f.close() #close xyz file

lidar.set_motor_pwm(0)  
mc.zaxis(1,1,frequency*4,m1,m2,50, (timeperrev+(zaxisruntime*3))/8) #zaxis return to start

mc.cutpower()  #close out 
spi.close() #close out 
print("hit enter to end",)
pause=input() #close out 
lidar.stop()#close out 
lidar.disconnect() #close out 