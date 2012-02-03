import os
import serial

try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/ttyUSB0', 9600);
except:
    print "Failed to connect"
    exit()

while True:
    print arduino.readline();
