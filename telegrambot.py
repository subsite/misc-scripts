#!/usr/bin/python

# Sends messages to Telegram Bot API. See https://core.telegram.org/bots/api for details.
# 
# Install: run as root (sudo) to create conf file
# Dependencies: python python-requests
#
# Note: uses one system wide api_token only. Not meant for multi-user environments.
#
# Fredrik Welander 2016
#

import os
import sys
import requests
import socket
import ConfigParser

usage = "USAGE: telegrambot.py MESSAGE"
config = ConfigParser.ConfigParser()   
configFile = "/etc/telegrambot.conf"

if len(config.read(configFile)) != 1:
	if os.geteuid() == 0:
		if raw_input("Run setup? [Y/n]: ").lower() not in [ 'y', '' ]:
			exit(0)
	    
		cfgfile = open(configFile,'w')
		config.add_section('main')
		api_token = raw_input("Enter Telegram Bot API token: ").strip()
		config.set('main', 'api_token', api_token)
		config.write(cfgfile)
		cfgfile.close()
		os.chmod(configFile, 0640)
		os.chown(configFile, 0, 4)
		print "Config file created with permissions -rw-r----- and ownership: root.adm. Setup complete."
		print usage
		exit(0)
	else:
		print "Config file {0} not found. Run as root for setup".format(configFile)
		exit(1)

if len(sys.argv) < 2:
	print usage
	sys.exit(1)

hostname = socket.gethostname()
token = config.get('main', 'api_token')
message = "*{0}:* {1}".format(hostname, sys.argv[1])

def botcall(method, data={}):
	return requests.get(
		url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
		params=data
	).json()
	return

chat_id = botcall("getUpdates")["result"][-1]["message"]["chat"]["id"]

botcall("sendMessage", {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})


