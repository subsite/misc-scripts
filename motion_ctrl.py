#!/usr/bin/python


import os
import signal
import time
import subprocess
import glob

motion = None

# Read motion.conf
motion_config = open(os.path.expanduser('~/.motion/motion.conf'))
statusfile = os.path.expanduser('~/.motion/EVENT_END')
unlock_time = time.time()

# Get target_dir from motion.conf
for line in motion_config:
    if line.startswith("target_dir"):
        target_dir = line.split(" ", 1)[1].strip()
        break

while(True):
    is_locked = subprocess.check_output([
            "qdbus", 
            "org.gnome.ScreenSaver", 
            "/com/canonical/Unity/Session", 
            "com.canonical.Unity.Session.IsLocked"]).strip()
    
    # Screen is locked, run motion (wait 30 secs)
    if is_locked == "true": # string not real bool
        # Start motion if not running already
        if not motion:
            if not lock_time:
                lock_time = time.time()
            # Start motion after locked for a while (don't record yourself leaving)
            elif time.time()-lock_time > 60:
                print "starting motion"
                motion = subprocess.Popen("/usr/bin/motion") 

    # Screen is unlocked, disable motion
    else:
        lock_time = None
        if motion: 
            print "Unlocked, motion stopped"
            unlock_time = time.time()
            motion.terminate()
            motion.wait()
            motion = None 
    
    # Check for statusfile
    if os.path.isfile(statusfile):
        os.remove(statusfile)
        # Send message about motion, but not if unlock is too recent
        if time.time()-unlock_time > 60:
            newest_img = max(glob.iglob(os.path.join(target_dir, '*.jpg')), key=os.path.getctime)
            os.system('telegrambot.py "(motion_ctrl) Motion detected" "{0}"'.format(newest_img))


    time.sleep(2)


