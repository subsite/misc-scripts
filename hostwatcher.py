#!/usr/bin/python

# Ping hosts and receive message if host doesn't answer
# 
# #example /etc/hostwatcher.conf:
# [main]
# # messenger should take the fail message as its first argument
# messenger = "/usr/local/sbin/telegrambot.py"
#
# [hosts]
# ping = [ "google.com", "facebook.com" ]
# ping6 = [ "ipv6.google.com", "facebook.com" ]
# http = [ "www.google.com" ]

import os
import json
import ConfigParser

# Init config
config = ConfigParser.RawConfigParser()   
configFile = "/etc/hostwatcher.conf"
config.read(configFile)
failmessage = "does not answer"

host_types = config.items( "hosts" )
for ping, hosts in host_types:
    for host in json.loads(hosts):
      if ping == "http":
        response =  os.system("nc -z -w2 " + host + " 80")
      else:
        response = os.system(ping + " -c 1 -w 1 " + host + " > /dev/null 2>&1")
      
      if response != 0:
        message = "{0} {1} {2}.".format(host, failmessage, ping)
        print message
        os.system('{0} "(hostwatcher) {1}"'.format(config.get('main', 'messenger'), message))
        

