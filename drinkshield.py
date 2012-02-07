import subprocess
import serial

ARG_MSG = "message"
SENSOR_FLAG = "foo"
SENSOR_READING = "bar"
SOBER_CMD = "git commit -a -m"
TOO_DRUNK_CMD = "git stash save"
MAX_DRUNKNESS = 100
MIN_DRUNKNESS = 10


try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
except:
    print "Failed to connect"
    exit()

while True:
    line = arduino.readline()
    print line

    if line.find(SENSOR_FLAG) > -1:
        print "found reading for BAC"
        readings = line.split(SENSOR_READING)
        BAC = ' '.join(readings)

        commit = SOBER_CMD + " " + ARG_MSG + " BAC:" + BAC

        print commit;
        #subprocess.call(commit, shell=True)
