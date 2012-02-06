import subprocess
import serial

ARG_MSG = "message"
SENSOR_FLAG = "foo"
SENSOR_READING = "bar"
SOBER_CMD = "git commit -a -m"
TOO_DRUNK_CMD = "git stash save"


try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/ttyUSB0', 9600);
except:
    print "Failed to connect"
    exit()

while True:
    line = arduino.readline();
    print line;

    if line.find(SENSOR_FLAG) > -1:
        print "found reading for BAC";
        BAC = line.substr(SENSOR_READING);

        commit = SOBER_CMD + " " + ARG_MSG + BAC;

        #subprocess.call(commit, shell=True);
