#!/usr/bin/python3

# Check SSL-site for certificate expiry. Uses the same conf file as
# hostwatcher.py, all sites in the "https" array
#
# #example /etc/hostwatcher.conf:
# [main]
# # messenger should take the fail message as its first argument
# messenger = "/usr/local/sbin/telegrambot.py"
#
# [hosts]
# https = [ "www.google.com" ]

import os
import json
import configparser
import shutil
import subprocess

########### 
# Init config
#
configFile = "/etc/hostwatcher.conf"
warning_days = 14
failmessage = "SSL-certificate expiring in {} days or less:".format(warning_days) 
cert_checker = ["ssl-cert-check", "-p", "443", "-n", "-q", "-x", str(warning_days), "-s"]
#
########### 

config = configparser.ConfigParser() 
config.read(configFile)
ssl_hosts = json.loads(config.get('hosts', 'https'))
messenger = config.get('main', 'messenger').replace('"', '')
cert_alert = False

if not shutil.which(cert_checker[0]):
  cert_alert = True
  err = "No cert checker found, hint: apt install ssl-cert-check"
  subprocess.call([messenger, err])
  exit(err)

for host in ssl_hosts:
  cert_check = subprocess.run(cert_checker + [host])

  if cert_check.returncode:
    cert_alert = True
    failmessage = "{} {}".format(failmessage,host)
  
if cert_alert:
  print(failmessage)
  subprocess.call([messenger, failmessage + ("certwatcher")])
        

