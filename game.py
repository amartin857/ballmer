#!/usr/bin/python

import yaml
import sys
import subprocess
import serial

f = open('config.yaml')
config = yaml.load(f);
f.close();

#some levels
MAX_DRUNKENNESS = config['game_max_drunk']
MIN_DRUNKENNESS = config['game_min_drunk'] 

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
        args = "-F crop --metal -f bigmono12.tlf --termwidth"
    cmd = "toilet " + args + " \""+msg+"\"";
    subprocess.call(cmd, shell=True)

t_print("party time", True);

# arduino connection
try:
    print "Get ready to blow..."
    arduino = serial.Serial('/dev/cu.usbmodem641', 9600)
except:
    print "Arduino Fail. Go home, you must be drunk."
    exit();


last_reading = 0;

# serial listening loop
while True:
    line = arduino.readline()

    if ( len(line) > 0 ):

        BAC = getReadingFromLine(line)

        if BAC > 0 and BAC != last_reading:
            subprocess.call("clear", shell=True);
            last_reading = BAC

            # not drunk enough
            if isTooSober( BAC ):
                t_print( str(BAC), False);
                print "You blew a " + str(BAC);
                print "You could use another drink!"

            # you might be in the Ballmer Peak 
            elif isSoberEnough( BAC ):
                t_print( str(BAC), False);
                print "You blew a " + str(BAC);
                print "Not bad!"

            # you have a problem (3 problems if you're committing RegEx)
            else: 
                t_print( str(BAC), False);
                print "You blew a " + str(BAC);
                t_print( " ", False);
                t_print("HELL YEAH", True);
                t_print("BRO BEANS", True);

