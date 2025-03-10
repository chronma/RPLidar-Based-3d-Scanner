# RPLidar-Based-3d-Scanner v3
Python code for Beaglebone Green Wireless - 3d Area Scanning
project can be found @ https://www.hackster.io/chronma/rplidar-based-3d-area-scanner-3ae946#things

main scanning file is 3d scanner 3d_Scanner_v3.py (Sudo python3 3d_Scanner_v3.py)
pylidartest runs link test and gives diagnostics from rplidar. run this if serial link terminates unexpectedly and errors are generated trying to reconnnect.

Changes this version.
Eliminates the angle sensor on the z axis drive. Uses the BB PRU (PRU1) to drive steps for motor. no feed back. practically give about the same angualy resolution.
Cleaned up the code a bit.

THe BB eproms are not reliable if left to sit.  This version keeps the operating system on an SD card and does not use the eprom.  The later BB images actually will resize your partion to matchthe free space on your sd card, which frees up quite a bit of room for scan files and such.
