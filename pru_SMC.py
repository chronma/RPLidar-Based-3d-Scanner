# python 3
#motor control
import ctypes
from ctypes import *
import Adafruit_BBIO.GPIO as GPIO
import time
import os
import mmap
import math
import subprocess

# NOTES

#USES PRU to generate stepper pulses and direction 

# globals

Task= ['getbit','setbit', 'clearbit']
#acess pru/arm shared memory   
DMEM_Offset=0x0002000  #pru DMEM
PRU1_Address=0x4a300000  #pru1 base address
Address=(DMEM_Offset+PRU1_Address)

fd = os.open("/dev/mem", os.O_SYNC | os.O_RDWR)
mem1 = mmap.mmap(fd, mmap.PAGESIZE, flags=mmap.MAP_SHARED, offset=Address)
os.close(fd)
command_bits=0
command_bits0=0
command_bits1=0
command_bits2=0

#Axis 4 - azimuth axis
Axis4_microsteps=8    #tbd
Axis4_ratio= 32  #gearbox*gear ratio
Axis4_motor_deg_per_step=.9
Axis4_direction_bit=3
Axis4_command_bit=0
Axis4_deg_per_step=Axis4_motor_deg_per_step/Axis4_ratio

#PRU1 steppercontrolpru1.out is set up for these pru outputs and inputs 
# Only need axis 4
subprocess.run("config-pin P8_45 pruout", shell=True, check=True)  #axis 4 pulses
subprocess.run("config-pin P8_46 pruout", shell=True, check=True)  #axis 4 dir
# subprocess.run("config-pin P8_43 pruout", shell=True, check=True)  #axis 5 pulses
# subprocess.run("config-pin P8_44 pruout", shell=True, check=True)  #axis 5 dir
# subprocess.run("config-pin P8_41 pruout", shell=True, check=True) #axis 6 pulses
# subprocess.run("config-pin P8_42 pruout", shell=True, check=True)  #axis 6 dir
# subprocess.run("config-pin P8_39 pruin", shell=True, check=True)  #limit
# subprocess.run("config-pin P8_40 pruin", shell=True, check=True)  #limit
# subprocess.run("config-pin P8_27 pruin", shell=True, check=True)   #limit
        
subprocess.run("echo 'stop' > /sys/class/remoteproc/remoteproc2/state", shell=True, check=False)
subprocess.run("sudo cp /home/debian/bin/Steppercontrolpru1.out /lib/firmware/Steppercontrolpru1.out", shell=True, check=True)
subprocess.run("echo 'Steppercontrolpru1.out' > /sys/class/remoteproc/remoteproc2/firmware", shell=True, check=True)
subprocess.run("echo 'start' > /sys/class/remoteproc/remoteproc2/state", shell=True, check=True) 
             
#stepper driver    

subprocess.run("config-pin P9_13 gpio", shell=True, check=True)  #
subprocess.run("config-pin P9_23 gpio", shell=True, check=True)  #
subprocess.run("config-pin P9_25 gpio", shell=True, check=True)  #  
        
GPIO.setup("P9_13", GPIO.OUT) #enable
GPIO.setup("P9_23", GPIO.OUT) #M1
GPIO.setup("P9_25", GPIO.OUT) #M2

def bitmagic(value, bitnumber,task):
    if task == 'getbit':
        return ((value>>bitnumber)&1)
    if task == 'setbit':
        return (value | (1<<bitnumber))
    if task == 'clearbit':
        return (value & ~(1<<bitnumber))
    
    if task =='TogleBit':
        return (value ^((value>>bitnumber)&1))

class motorcontrol(object):
    #globals for testing
    
    # intitialize
    def __init__(self):
       def __init__(self):

 
        print ("initilized")
    
    # destructor
    def __del__(self):
        
        #stepper driver
        GPIO.output("P9_13",1) #enable
        GPIO.output("P9_23",0) #M1
        GPIO.output("P9_25",0) #M2
           
        print ('end')

    def cutpower(self):
        
         #stepper driver
               
        GPIO.output("P9_13",1) #enable
        GPIO.output("P9_23",0) #M1
        GPIO.output("P9_25",0) #M2
        
        print ('end')
        
    def zaxis(self,pru1_command_bits,a4degrees,a4degreespersec,a4acceltime, m1,m2,multiplier):    
        
        #stepper driver
        GPIO.output("P9_13",0) #enable
        GPIO.output("P9_23",m1) #M1
        GPIO.output("P9_25",m2) #M2
        # M2  M1 Steps
        # 0   1   1/2
        # 1   0   1/4
        # 0   0   1/8
        # 1   1   1/16

        #pru1
        pru1_command_bits=0
        a4steps=int((abs(a4degrees))/(Axis4_deg_per_step/multiplier)) #run the 
        print ('steps', a4steps)
        a4pulselength=int((1/a4degreespersec)*(Axis4_deg_per_step/multiplier)*200000000) #set frequency
        print('pulselength',a4pulselength)
        a4adsteps=int(math.sqrt( (8*(a4acceltime*1000000000)+a4pulselength)/(4*a4pulselength))+.5) #no accel /decel
        print('accel steps ',a4adsteps)
        ctypes.c_uint32.from_buffer(mem1, 0x300).value = a4steps
        ctypes.c_uint32.from_buffer(mem1, 0x304).value = a4pulselength 
        ctypes.c_uint32.from_buffer(mem1, 0x318).value = a4adsteps
        if (a4degrees<0):
            pru1_command_bits=bitmagic(pru1_command_bits,Axis4_direction_bit,'setbit') # 
        else:
             pru1_command_bits=bitmagic(pru1_command_bits,Axis4_direction_bit,'clearbit')
        
        pru1_command_bits=bitmagic(pru1_command_bits,Axis4_command_bit,'setbit') # 
        print(hex(pru1_command_bits))
        time.sleep(.1)
        ctypes.c_uint32.from_buffer(mem1, 0x200).value = pru1_command_bits
        time.sleep (.01)
        done =False
        while not done:
            pru_command_bits=ctypes.c_uint32.from_buffer(mem1, 0x200).value #send command word to the PRU shared memory
            #print("pru1 ", end=' ')
            #for i in range (31,-1,-1):
            #    print(bitmagic(pru_command_bits,i,'getbit'), end='')
            #print(' ')
            if ((bitmagic(pru_command_bits,9,"getbit")==0) and (bitmagic(pru_command_bits,10,"getbit")==0) and (bitmagic(pru_command_bits,11,"getbit")==0) ): 
                done=True
            time.sleep(.001)
           
        return (pru1_command_bits)       
        
        
        
    
            
            
        