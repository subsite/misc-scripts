#!/usr/bin/python

# Sends messages as a Telegram Bot. 
# See: https://core.telegram.org/bots#3-how-do-i-create-a-bot for details
# 
# Install: run as root (sudo) to create conf file
# Dependencies: python python-requests
#
# Note: Uses one system wide api_token only. Not meant for multi-user environments.
# Note: There's no stopping anyone from adding this bot to their Telegram. 
#       The messages will however only go to the chat_id in the config file
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
hostname = socket.gethostbyaddr(socket.gethostname())[0]

# Init config
config = ConfigParser.ConfigParser()   
configFile = "/etc/telegrambot.conf"

# Request function
def botcall(method, token, data={}):
	response = requests.get(
		url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
		params=data
	).json()
	if not response["ok"]:
		print "Telegrambot request error: {0} {1}".format(response["error_code"], response["description"])
		exit(1)
	return response

# Check if config file exists
if len(config.read(configFile)) != 1:
	# Check if run by root
	if os.geteuid() == 0:
		if raw_input("Run setup? [Y/n]: ").lower() not in [ 'y', '' ]:
			exit(0)
	    
		token = raw_input("Enter Telegram Bot API token: ").strip()
		bot_uname = botcall("getMe", token)["result"]["username"]
		print "Bot {0} found. Getting last chat_id...".format(bot_uname)

		config.add_section('main')
		config.set('main', 'api_token', token)
		config.set('main', 'bot', bot_uname)

		# Request: get chats for bot
		chats = botcall("getUpdates", token)["result"]
		if len(chats) == 0:
			print "No chats found. Open telegram.me/{0} in Telegram and press Start, then re-run Setup.".format(bot_uname)
			exit(1)

		# Get last chat id
		last_chat = chats[-1]["message"]["chat"]
		if raw_input("Found chat_id {0} for user {1} {2}. Is this correct? [Y/n]: "
			.format(
				last_chat["id"], 
				last_chat["first_name"], 
				last_chat["last_name"])).lower() not in [ 'y', '' ]:
			exit(0)
		config.set('main', 'chat_id', last_chat["id"])

		# Write to config file
		cfgfile = open(configFile,'w')
		config.write(cfgfile)
		cfgfile.close()
		os.chmod(configFile, 0640)
		os.chown(configFile, 0, 4)

		print "Config file created with permissions '-rw-r-----' and ownership 'root.adm'."
		print "Change permissions as needed or just add yourself to group adm. Guard your token."
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
chat_id = config.get('main', 'chat_id')
message = "[{0}]: {1}".format(hostname, sys.argv[1])

# Request 2/2, send message
botcall("sendMessage", token, { "chat_id": chat_id, "text": message })


