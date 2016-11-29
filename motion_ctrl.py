#!/usr/bin/python


import os
import signal
import time
import subprocess
import glob
import gtk
import appindicator
from threading import Thread # https://pymotw.com/2/threading/




# Read motion.conf
motion_config = open(os.path.expanduser('~/.motion/motion.conf'))
statusfile = os.path.expanduser('~/.motion/EVENT_END')


# Get target_dir from motion.conf
for line in motion_config:
    if line.startswith("target_dir"):
        target_dir = line.split(" ", 1)[1].strip()
        break


# Create Ubuntu appindicator
def init_indicator():
    print "init_indicator"
    indicator = appindicator.Indicator("my-indicator", 'camera-web', appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_menu(build_menu())
    watcher=Thread(target=motion_watcher)
    watcher.setDaemon(True)
    watcher.start()
    gtk.main()
    

# Create the indicator menu
def build_menu():
    print "build_menu"
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
    print "motion_watcher"
    while True:
        print "main loop"
        time.sleep(2)
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

        

indicator_thread=Thread(target=init_indicator)
indicator_thread.start()






#main_thread.join()
#watcher.join()

