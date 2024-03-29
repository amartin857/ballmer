#!/usr/bin/python

import yaml
import sys
import subprocess
import serial

f = open('config.yaml')
config = yaml.load(f);
f.close();

# too shitfaced to commit code?
# or not shitfaced enough? 
MAX_DRUNKENNESS = config['demo_max_drunk']
MIN_DRUNKENNESS = config['demo_min_drunk'] 

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

def buildCommit( BAC ):
    commit_message = ""
    if len(sys.argv) > 2:
        commit_message += ( sys.argv[2] + " DRUNK_LEVEL:" + str(BAC) );
    else:
        commit_message = "BAC: " + str(BAC);
    return "git commit -a -m " + "\"" + commit_message + "\"";

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

t_print("party time", True);
t_print("git commit", True);

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

# serial listening loop
while True:
    line = arduino.readline()

    if ( len(line) > 0 ):

        BAC = getReadingFromLine(line)

        if BAC > 0:

            # Test mode
            if  sys.argv[1] == "test":
                t_print( str(BAC), False );
                print "Your drunkenness level is only " + str(BAC)
                exit();

            # Commit mode
            elif sys.argv[1] == "commit":
                print "Your drunkenness level is " + str(BAC)

                # not drunk enough
                if isTooSober( BAC ):
                    print "Looks like you could use another drink!"
                    print "Commiting your sober code"
                    subprocess.call(buildCommit( BAC ), shell=True)
                    exit();

                # you might be in the Ballmer Peak 
                elif isSoberEnough( BAC ):
                    print "You seem sober enough to commit code."
                    subprocess.call(buildCommit( BAC ), shell=True)
                    exit();

                # you have a problem (3 problems if you're committing RegEx)
                else: 
                    print "Nothing committed."
                    print "Your changes have been stashed for tomorrow..."
                    t_print("GO HOME", False);
                    t_print("YOU ARE", False);
                    t_print("DRUNK", False);
                    subprocess.call("git stash save", shell=True)
                    exit();

            # You can't type 
            else:
                print "wtf is \"" + sys.argv[1] + "\"? Try \"commit\" or \"test\" or try sobering up."
                exit();

