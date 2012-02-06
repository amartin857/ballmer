import subprocess
import serial

SENSOR_FLAG = "foo"
SENSOR_READING = "bar"
COMMIT_ARGS  = "-a -m"
SOBER_CMD = "git commit"
TOO_DRUNK_CMD = "git stash save"

try:
    print "Get ready to blow..."
    subprocess.call("git status");
    arduino = serial.Serial('/dev/ttyUSB0', 9600);
except:
    print "Failed to connect"
    exit()

while True:
    line = arduino.readline();
    print line;

    if line.find(SENSOR_FLAG) > -1:
        print "found reading for BAC";
