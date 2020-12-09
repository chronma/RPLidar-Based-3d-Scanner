import time
import math
import subprocess
import spidev
import Adafruit_BBIO.GPIO as GPIO     

def getfilename():
    datestamp=str(time.localtime()[0]).zfill(2)+"_"+ str(time.localtime()[1]).zfill(2)+ "_" +str(time.localtime()[2]).zfill(2)
    timestamp = " " + str(time.localtime()[3]).zfill(2)+"."+str(time.localtime()[4]).zfill(2) +"."+str(time.localtime()[5]).zfill(2)
    
    path="/home/debian/sdc/"
    filename=path+datestamp+timestamp
    #filename=datestamp+timestamp+rootname
    return filename
#TMC2209 MS2, MS1: 00: 1/8, 01: 1/32, 10: 1/64 11: 1/16
def getzaxisruntime(frequency,motorsteps,driveratio,m1,m2,zaxisindex, Nscancycles):
    pi=math.pi #pi constant
    #factor =1.021
    #factor = 1+(.0000060*zaxisindex) #.0000100 works for 1500 steps/rev
    #factor = 1+(.0000050*zaxisindex) #.0000050 works for 4500 steps/rev
    factor = 1+(.0000052*zaxisindex) #.0000050 works for 6000 steps/rev
    if m2 == 0 and m1 == 0: #1/8 step
        multiplier=8
    if m2==0 and m1 == 1: #1/2 step
        multiplier=32  
    if m2==1 and m1 == 0: #1/4 step
        multiplier=64
    if m2==1 and m1 == 1: #1/16 step
        multiplier=16
    Nstepsperrev=driveratio*motorsteps*multiplier # physical steps per rev 1.8 deg stepper motor drive ratio is 8*200*16 (3200*)
    timeperrev=Nstepsperrev/frequency
    zaxisanglestep=2*pi/zaxisindex 
    zaxisruntime=factor*timeperrev/zaxisindex
    return zaxisruntime

class anglesensor:
    
    def __init__(self, port0, port1, spimode):
        #subprocess call (set gpio pins)
        subprocess.check_call("config-pin p9.17 spi_cs",shell=True)
        subprocess.check_call("config-pin p9.22 spi_sclk",shell=True)
        subprocess.check_call("config-pin p9.21 spi",shell=True)
        subprocess.check_call("config-pin p9.18 spi",shell=True)
        subprocess.check_call("config-pin p9.24 gpio",shell=True)
        subprocess.check_call("clear",shell=True)
        self.spi=spidev.SpiDev()
        self.spi.close()
        self.spi.open(port0,port1)
        self.spi.mode=spimode
        GPIO.setup("P9_24", GPIO.OUT) #mosi set to 1 for 3 wire mode

    def close(self):
        self.spi.close()
    
    def getangle(self):
        
        anglestep=0.02197265625 #degrees per count
        self.spi.cshigh=False
        GPIO.output("P9_24",1) #enable
        #time.sleep(.05)
        numbertoaverage=5
        vread=self.spi.readbytes(2)
        summed=int.from_bytes(vread, "big")% 2**14
        vreadstart=summed
        count=0
        count1=0
        while count<numbertoaverage:
            time.sleep(.001)
            self.spi.cshigh=False
            vread=self.spi.readbytes(2)
            vreadint=int.from_bytes(vread, "big")% 2**14
            
            if vreadstart<6 and vreadstart>=0:
                if vreadint<10:
                    summed=summed+vreadint
                    count1 +=1
                    
            
            if vreadstart<16384 and vreadstart>16378:
                if vreadint>16300:
                    summed=summed+vreadint
                    count1 +=1
                            
            if vreadstart<=16378 and vreadstart>=6:
                summed=summed+vreadint
                count1 +=1
                
            count +=1
            
            
            self.spi.cshigh=True
        average=summed/(count1+1)
        return (average*anglestep)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

""" # this is for old stepper drivers
def getzaxisruntime(frequency,motorsteps,driveratio,m1,m2,m3,zaxisindex, Nscancycles):
    pi=math.pi #pi constant
    if m1==0 and m2 == 0 and m3==0: #full step
        multipier=1
    if m1==1 and m2 == 0 and m3==0: #half step
        multipier=2  
    if m1==0 and m2 == 1 and m3==0: #quarter step
        multipier=4
    if m1==1 and m2 == 1 and m3==0: #eighth step
        multiplier=8
    if m1==0 and m2 == 0 and m3==1: #16th step
        multiplier=16
    if m1==1 and m2 == 1 and m3==1: #32nd step (othercombos too)
        multiplier=32  
    Nstepsperrev=driveratio*motorsteps*multiplier # physical steps per rev 1.8 deg stepper motor drive ratio is 8*200*16 (3200*)
    timeperrev=Nstepsperrev/frequency
    zaxisanglestep=2*pi/zaxisindex 
    zaxisruntime=timeperrev/zaxisindex
    return zaxisruntime
    """