#!/usr/bin/python3

import os
import shutil
import sys
import zipfile

default_size = 10
default_saves = 3

# Check arguments
if len(sys.argv) < 2:
    exit("USAGE: logrotate.py [filepath] [treshold size MB (optional default {}MB)]".format(default_size))


logfile = sys.argv[1]
maxsize = sys.argv[2] if len(sys.argv) > 2 else default_size

if not os.path.isfile(logfile):
    exit("No logfile found.")

cursize = round(os.path.getsize(logfile) / 1000000)


for i in range(default_saves,0,-1):
    print(i)
    try:
        shutil.copy2("{}.{}".format(logfile, i-1), "{}.{}".format(logfile, i))
    except:
        print("{}.{} Not found.".format(logfile, i))

    if i == 1:
        shutil.copy2(logfile, "{}.0".format(logfile))
        open(logfile, 'w').close()


