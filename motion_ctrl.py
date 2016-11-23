#!/usr/bin/python


import os
import commands
import time

while 1 == 1:

    islocked = commands.getstatusoutput('qdbus org.gnome.ScreenSaver /com/canonical/Unity/Session com.canonical.Unity.Session.IsLocked' )
    print islocked
    time.sleep(2)

print "screen unclocked"
