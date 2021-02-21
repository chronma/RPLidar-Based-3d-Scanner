# A basic, from scratch, test for a rotary sensor on a Raspberry Pi
# You need to enable the SPI bus by running raspi-config
import time
import spidev
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, 1) #Sets MOSI to one for readonly mode on the 5048A
# Only SPI bus 0 is available on the Pi
bus = 0
# Device is the chip select pin. Set to 0 (GPIO8, Pin24) or 1 (GPIO7, Pin26)
device = 0
# Enable SPI
spi = spidev.SpiDev()
spi.open(bus, device)
# Set SPI speed and mode
spi.max_speed_hz = 1000000
spi.mode = 0b01 #The 5048A uses spi mode 1
anglestep=0.02197265625 #degrees per count, the fiddle factor used to get degrees for the 5048A
vread = spi.readbytes(2) # Throw first reading away
try:
    while True:
        vread = spi.readbytes(2)       
        angle=int.from_bytes(vread, "big")% 2**14
        angle = (angle * anglestep)
        print("Angle is: ", round(angle, 2))
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    spi.close()
