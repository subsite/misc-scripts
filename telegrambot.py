#!/usr/bin/python

# Sends messages as a Telegram Bot. 
# See: https://core.telegram.org/bots#3-how-do-i-create-a-bot for details
# 
# Install: run as root (sudo) to create conf file
# Dependencies: python python-requests
#
# Note: uses one system wide api_token only. Not meant for multi-user environments.
# 
# USAGE: telegrambot.py "MESSAGE" 
# (MESSAGE supports markdown) 
#
# Fredrik Welander 2016
#

import os
import sys
import socket
import ConfigParser
# request seems not to be installed by default on Debian/Ubuntu, check for it
try:
	import requests
except ImportError:
	print "Unmet dependencies. Install python-requests"
	exit(1)

usage = 'USAGE: telegrambot.py "MESSAGE"'
hostname = socket.gethostname()

# Init config
config = ConfigParser.ConfigParser()   
configFile = "/etc/telegrambot.conf"

# Check if config file exists
if len(config.read(configFile)) != 1:
	# Check if run by root
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
		print "Config file created with permissions '-rw-r-----' and ownership 'root.adm'."
		print "Change permissions as needed or just add yourself to group adm."
		print "Setup complete."
		print usage
		exit(0)
	else:
		print "Config file {0} not found or no read permissions. Run as root for setup.".format(configFile)
		exit(1)

# Check for correct amount of args
if len(sys.argv) < 2:
	print usage
	sys.exit(1)

# Read api token from config
token = config.get('main', 'api_token')
message = "*{0}:* {1}".format(hostname, sys.argv[1])

# Request function
def botcall(method, data={}):
	response = requests.get(
		url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
		params=data
	).json()
	if not response["ok"]:
		print "Request error: {0} {1}".format(response["error_code"], response["description"])
		exit(1)
	return response

# Request 1/2, get chat_id
chat_id = botcall("getUpdates")["result"][-1]["message"]["chat"]["id"]

# Request 2/2, send message
botcall("sendMessage", {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})


