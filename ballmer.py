import os
import serial

try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/ttyUSB0', 9600);
except:
    print "Failed to connect"
    exit()

while True:
    line = arduino.readline();
    print line;

    if line.find("foo") > -1:
        print "o_0 you are drunk 0_o";
