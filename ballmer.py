#!/usr/bin/python

import sys
import subprocess
import serial

SENSOR_FLAG = "foo"
SENSOR_READING = "bar"
SOBER_CMD = "git commit -a -m"
TOO_DRUNK_CMD = "git stash save"
MAX_DRUNKNESS = 100
MIN_DRUNKNESS = 10

if len(sys.argv) == 1:
    print "No action taken. Use 'ballmer test' or 'ballmer commit [message]'";
    exit();

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
        BAC = "foo" #TODO: actually populate this

        if  sys.argv[1] == "test":
            print "Your BAC Level is {something}"

        elif sys.argv[1] == "commit":
            commit_message = ""

            if len(sys.argv) > 2:
                commit_message += (sys.argv[2] + " BAC:" + BAC)

            #TODO: split sober command with drunk one based on MAX

            #subprocess.call(commit, shell=True)
