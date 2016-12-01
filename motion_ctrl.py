#!/usr/bin/python

# Starts motion (https://github.com/Motion-Project/motion) when screen is locked. 
# Sends message with image of detected motion using telegrambot 
# (https://github.com/subsite/misc-scripts/blob/master/telegrambot.py)
# 
# Note: Must be started in a Unity session, put in Startut Applications to launch at login
# Note: Set "daemon off" in motion.conf

import os
import signal
import time
import subprocess
import glob
import gtk
import appindicator
import logging
import threading 

# Set to True to show console ooutput for debug 
log_to_console = False

# Read motion.conf
motion_config = open(os.path.expanduser('~/.motion/motion.conf'))
statusfile = os.path.expanduser('~/.motion/EVENT_END')

# Set logging params
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

###########

def logput(msg):
    if log_to_console:
        logging.debug(msg)
    
# Get target_dir from motion.conf
for line in motion_config:
    if line.startswith("target_dir"):
        target_dir = line.split(" ", 1)[1].strip()
        break

# Needed for gtk to work with threading
gtk.threads_init()

# Create Ubuntu appindicator
def init_indicator():
    logput('init_indicator')
    indicator = appindicator.Indicator("my-indicator", 'camera-web', appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

# Create the indicator menu
def build_menu():
    logput('build_menu')
    menu = gtk.Menu()
    for menuitem in [["Motion Control"], ["Open folder", "open_folder"], ["Quit", "quit"]]:
        cur_item = gtk.MenuItem(menuitem[0])
        if len(menuitem) > 1:
            cur_item.connect('activate', menuitem_response, menuitem[1]) # Event listener
        else:
            cur_item.set_sensitive(False) # "grayed out"

        menu.append(cur_item)

    menu.show_all()
    return menu

# Handle event
def menuitem_response(self, action):
	if action == "open_folder":
		subprocess.call(["/usr/bin/xdg-open", target_dir])
	elif action == "quit":
		quit()


# Motion watcher
def motion_watcher():
    motion = None
    unlock_time = time.time()
    logput('motion_watcher')
    is_locked = False
    while True:
        time.sleep(2)
        is_locked = subprocess.check_output([
            "qdbus", 
            "org.gnome.ScreenSaver", 
            "/com/canonical/Unity/Session", 
            "com.canonical.Unity.Session.IsLocked"]).strip()
        logput('is_locked:'+is_locked)
        
        # Screen is locked, run motion (wait 30 secs)
        if is_locked == "true": # string not real bool
            # Start motion if not running already
            
            if not motion:
                if not lock_time:
                    logput('not lock_time')
                    lock_time = time.time()
                # Start motion after locked for a while (don't record yourself leaving)
                elif time.time()-lock_time > 60:
                    logput('starting motion')
                    motion = subprocess.Popen("/usr/bin/motion") 

        # Screen is unlocked, disable motion
        else:
            logput('screen is unlocked')
            lock_time = None
            if motion: 
                logput('Unlocked, motion stopped')
                unlock_time = time.time()
                motion.terminate()
                motion.wait()
                motion = None 
        
        # Check for statusfile
        if os.path.isfile(statusfile):
            os.remove(statusfile)
            # Send message about motion, but not if unlock is too recent
            if time.time()-unlock_time > 60:
                logput('Send message')
                newest_img = max(glob.iglob(os.path.join(target_dir, '*.jpg')), key=os.path.getctime)
                os.system('telegrambot.py "(motion_ctrl) Motion detected" "{0}"'.format(newest_img))


# Start watcher in daemon thread        
w = threading.Thread(name='motion_watcher', target=motion_watcher)
w.setDaemon(True)
w.start()

# Start main thread
init_indicator()


