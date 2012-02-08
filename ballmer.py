#!/usr/bin/python

import sys
import subprocess
import serial

# how shitfaced must you be to refuse a commit?
MAX_DRUNKENNESS = 100

# you need to pass an arg 
if len(sys.argv) == 1:
    print "No action taken. Use 'ballmer test' or 'ballmer commit [message]'";
    exit();

# arduino connection
try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/cu.usbmodem641', 9600)
except:
    print "Arduino Fail. Go home, you must be drunk."
    exit();

# helper functions
def isSoberEnough( BAC ):
    if BAC < MAX_DRUNKENNESS:
        return True
    else:
        return False

def buildCommit( BAC ):
    commit_message = ""
    if len(sys.argv) > 2:
        commit_message += (sys.argv[2] + " BAC:" + BAC)
    return "git commit -a -m " + "\"" + commit_message + "\"";

def getReadingFromLine( line ):
    return int(float(line)); 

# serial listening loop
while True:
    line = arduino.readline()
    print line #TODO: rm this after debug

    #BAC = getReadingFromLine(line)
    BAC = 0;

    #TODO: need to set some kind of timeout
    if BAC > 1:
        print "found reading for BAC" #TODO: rm this after debug

        # Test mode response
        if  sys.argv[1] == "test":
            print "Your drunkenness level is {something}"
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

