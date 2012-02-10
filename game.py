#!/usr/bin/python

import sys
import subprocess
import serial

# helper functions
def isTooSober( BAC ):
    if BAC < MIN_DRUNKENNESS:
        return True
    else:
        return False

def isSoberEnough( BAC ):
    if BAC < MAX_DRUNKENNESS:
        return True
    else:
        return False

def getReadingFromLine( line ):
    segment = line[9:]
    if len(segment) > 0:
        return float(segment); 
    else:
        return 0;

def t_print( msg, hasColor ):
    if hasColor:
        args = "-F crop --gay --termwidth"
    else:
        args = "-F crop --metal -f ascii12.tlf --termwidth"
    cmd = "toilet " + args + " \""+msg+"\"";
    subprocess.call(cmd, shell=True)

t_print("pary time", True);

# arduino connection
try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/cu.usbmodem641', 9600)
except:
    print "Arduino Fail. Go home, you must be drunk."
    exit();

# serial listening loop
while True:
    line = arduino.readline()

    if ( len(line) > 0 ):

        BAC = getReadingFromLine(line)

        if BAC > 0:

            # not drunk enough
            if isTooSober( BAC ):
                t_print( str(BAC), False);

            # you might be in the Ballmer Peak 
            elif isSoberEnough( BAC ):
                t_print( str(BAC), False);

            # you have a problem (3 problems if you're committing RegEx)
            else: 
                t_print( str(BAC), False);
                t_print("HELL YEAH", True);
                t_print("BRO BEANS", True);

