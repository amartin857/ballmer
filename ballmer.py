#!/usr/bin/python

import sys
import subprocess
import serial

SENSOR_FLAG = "foo"
SENSOR_READING = "bar"
MAX_DRUNKNESS = 100
MIN_DRUNKNESS = 10

if len(sys.argv) == 1:
    print "No action taken. Use 'ballmer test' or 'ballmer commit [message]'";
    exit();

try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
except:
    print "Failed to connect to Arduino."
    print "If you're too drunk to connect the USB cable, GO HOME"
    exit();

def isSoberEnough( BAC ):
    if BAC < MAX_DRUNKNESS:
        return True
    else:
        return False

def buildCommit( BAC ):
    commit_message = ""
    if len(sys.argv) > 2:
        commit_message += (sys.argv[2] + " BAC:" + BAC)
    return "git commit -a -m " + "\"" + commit_message + "\"";

def getReadingFromLine( line ):
    reading = "foo" #TODO: this
    return reading; #just a stub for now

while True:
    line = arduino.readline()
    print line

    if line.find(SENSOR_FLAG) > -1:
        print "found reading for BAC" #TODO: rm this after debug
        BAC = getReadingFromLine(line)

        # Test mode response
        if  sys.argv[1] == "test":
            print "Your BAC Level is {something}"
            exit();

        # Commit mode response
        elif sys.argv[1] == "commit":
            if isSoberEnough( BAC ):
                subprocess.call(buildCommit( BAC ), shell=True)
                exit();
            else: 
                subprocess.call("git stash save", shell=True)
                print "Nothing committed."
                print "Your changes have been stashed for tomorrow..."
                print "GO HOME YOU ARE TOO DRUNK"

        # You fucked up and/or can't type response
        else:
            print "wtf is \"" + sys.argv[1] + "\"? Try \"commit\" or \"test\" or try sobering up."
            exit();

