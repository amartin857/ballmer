#!/usr/bin/python

import sys
import subprocess
import serial

# too shitfaced to commit code?
# or not shitfaced enough? 
MAX_DRUNKENNESS = 100
MIN_DRUNKENNESS = 20

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
        commit_message += (sys.argv[2] + " BAC:" + BAC)
    return "git commit -a -m " + "\"" + commit_message + "\"";

def getReadingFromLine( line ):
    return float(line); 

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
        print BAC

        #TODO: need to set some kind of timeout
        if BAC > 0:
            print line #TODO: rm this after debug

            # Test mode
            if  sys.argv[1] == "test":
                print "Your drunkenness level is {something}"
                exit();

            # Commit mode
            elif sys.argv[1] == "commit":

                # not drunk enough
                if isTooSober( BAC ):
                    print "Looks like you could use another drink!"
                    print "Commiting your sober boring code"
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

