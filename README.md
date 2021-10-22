# RPLidar-Based-3d-Scanner
Modified RPlidar Code for a Raspberry Pi. This code was written by Chris Martin and has been modified to run on a Raspberry Pi. It has only been tested on a Raspberry Pi 3 and a Raspberry Pi 4 (4gb) but should work on other versions. The following programs have remained unchanged:- 
pylidar.py
pylidar_protocol.py
pylidar_serial.py
pylidar_serial.pyc
pylidartest.py

The main scanning program is pi_3d Scanner rplidar v1.py

Motor information
Uses a TMC2209 v3.0
Enable TMC2209(pin 1) to RPi GPIO24 (pin 18),
Direction TMC2209(pin8) to RPi GPIO23 (pin 16),
M1 TMC2209(pin 2) to RPi GPIO7 (pin 26),
M2 TMC2209(pin 3) to RPi GPIO25 (pin 22),
step TMC2209(pin 7) to RPi GPIO18 (pin 12)

Once you have it connected, run pi_stepper_test.py. Looking from the top, the scanner should rotate clockwise one full turn and then anitclockwise. The angle shown in the pi_stepper_test isn't from the angle sensor. Even after a few tests, the motor should remain cool. Adjust the current limit on the TMC2209 if the motor or driver gets too hot.

Sensor information
The angle sensor is on the spi bus 0, device 0
It uses:-
GPIO ports 10 (pin 19) MOSI (which is set to 1 for readonly mode)
GPIO port 9 (pin 21) MISO,
GPIO port11 (pin 23) SPIO Clock,
GPIO 8 (pin 24) for CE (active low)

Run raspi-config to enable the SPI bus

Once you have connected the sensor run the pi_angle_sensor_test.py. It will show you the sensor readout. Move the scanner slowly by hand. Remember it will rotate 8 times for one complete revolution of the scanner.

Sensor note
If you scan a square room and the image doesn't come out square or the calculated and measured angles are way out when scanning, then even if the sensor looks like it is working it isn't. The magnet has to be centred with very little wobble and must be VERY close to the sensor to work.
