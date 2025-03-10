import Adafruit_BBIO.GPIO as GPIO
import subprocess
import time

subprocess.run("config-pin P9_13 gpio", shell=True, check=True)  #
subprocess.run("config-pin P9_23 gpio", shell=True, check=True)  #
subprocess.run("config-pin P9_25 gpio", shell=True, check=True)  #  
        
GPIO.setup("P9_13", GPIO.OUT) #enable
GPIO.setup("P9_23", GPIO.OUT) #M1
GPIO.setup("P9_25", GPIO.OUT) #M2

while 1:
    GPIO.output("P9_13",1) #enable 
    GPIO.output("P9_23",1) #enable 
    GPIO.output("P9_25",1) #enable 
    time.sleep(1)
    GPIO.output("P9_13",0) #enable 
    GPIO.output("P9_23",0) #enable 
    GPIO.output("P9_25",0) #enable 
    time.sleep(1)
