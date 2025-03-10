import ctypes
from ctypes import *
import subprocess
import os
import mmap
import time


subprocess.run("echo 'stop' > /sys/class/remoteproc/remoteproc2/state", shell=True, check=False)
subprocess.run("sudo cp /home/debian/bin/Steppercontrolpru1.out /lib/firmware/Steppercontrolpru1.out", shell=True, check=True)
subprocess.run("echo 'Steppercontrolpru1.out' > /sys/class/remoteproc/remoteproc2/firmware", shell=True, check=True)
time.sleep(2)
subprocess.run("echo 'start' > /sys/class/remoteproc/remoteproc2/state", shell=True, check=True)

#PRU 1


subprocess.run("config-pin P8_45 pruout", shell=True, check=True)  #a4 pulse
subprocess.run("config-pin P8_46 pruout", shell=True, check=True)  #a4 dir
subprocess.run("config-pin P8_43 pruout", shell=True, check=True)  #a5 pulse
subprocess.run("config-pin P8_44 pruout", shell=True, check=True)  #a5 dir
subprocess.run("config-pin P8_41 pruout", shell=True, check=True)  #a6 pulse
subprocess.run("config-pin P8_42 pruout", shell=True, check=True)  #a6 dir

# need to run script from command line as sudo,sudo python3 ctypestest.py
Task= ['getbit','setbit', 'clearbit']

def bitmagic(value, bitnumber,task):
    if task == 'getbit':
        return ((value>>bitnumber)&1)
    if task == 'setbit':
        return (value | (1<<bitnumber))
    if task == 'clearbit':
        return (value & ~(1<<bitnumber))
    
    if task =='TogleBit':
        return (value ^((value>>bitnumber)&1))
    
a=0x0002000
b=0x4a300000
c=(a+b)
print (c)


a4steps=int(9900)
a4pulselength=int(100000)
a4adsteps=int(10)
a5steps=int(10000)
a5pulselength=int(1000000)
a5adsteps=int(10)
a6steps=int(999900)
a6pulselength=int(1000)
a6adsteps=int(10)

fd = os.open("/dev/mem", os.O_SYNC | os.O_RDWR)
mem = mmap.mmap(fd, mmap.PAGESIZE, flags=mmap.MAP_SHARED, offset=c)
os.close(fd)

command_bits = ctypes.c_uint32.from_buffer(mem, 0x200).value # 0x00 is the command bit

t=0
ctypes.c_uint32.from_buffer(mem, 0x200).value = t   

t=bitmagic(t,0,'setbit')
t=bitmagic(t,1,'setbit')
t=bitmagic(t,2,'setbit')
t=bitmagic(t,3,'setbit')
#t=bitmagic(t,4,'setbit')
#t=bitmagic(t,5,'setbit')
print (hex(t))
print (time.asctime())
for x in range(0,1,1):
    
    ctypes.c_uint32.from_buffer(mem, 0x300).value = a4steps
    ctypes.c_uint32.from_buffer(mem, 0x304).value = a4pulselength 
    ctypes.c_uint32.from_buffer(mem, 0x318).value = a4adsteps
    ctypes.c_uint32.from_buffer(mem, 0x308).value = a5steps
    ctypes.c_uint32.from_buffer(mem, 0x30C).value = a5pulselength 
    ctypes.c_uint32.from_buffer(mem, 0x31C).value = a5adsteps
    ctypes.c_uint32.from_buffer(mem, 0x310).value = a6steps
    ctypes.c_uint32.from_buffer(mem, 0x314).value = a6pulselength 
    ctypes.c_uint32.from_buffer(mem, 0x320).value = a6adsteps
    ctypes.c_uint32.from_buffer(mem, 0x200).value = t 
    

    command_bits = ctypes.c_uint32.from_buffer(mem, 0x200).value # 0x00 is the command bit
    print (hex(command_bits))
    
    h=0
    h1=0

    for x in range (0,3):
        if (bitmagic(command_bits,x,"getbit")==1):
            h=bitmagic(h,x,'setbit')
            h1=bitmagic(h1,x,'setbit')
        else:    
            h=bitmagic(h,x,'clearbit')
            h1=bitmagic(h1,x,'clearbit')
    print(hex(h1), hex(h))
    
    while ((h1!=0) or (h!=0)):
        time.sleep(.1)
        
        command_bits = ctypes.c_uint32.from_buffer(mem, 0x200).value # 0x00 is the command bit
        
        for x in range (0,3):
            if (bitmagic(command_bits,x,"getbit")==1):
                h=bitmagic(h,x,'setbit')
                h1=bitmagic(h1,x,'setbit')
            else:    
                h=bitmagic(h,x,'clearbit')
                h1=bitmagic(h1,x,'clearbit')
        
    time.sleep(1)
t=0
#ctypes.c_uint32.from_buffer(mem, 0x200).value = t 

