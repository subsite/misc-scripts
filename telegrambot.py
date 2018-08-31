#!/usr/bin/python3

# Sends messages as a Telegram Bot. 
# See: https://core.telegram.org/bots#3-how-do-i-create-a-bot for details
# 
# Install: run as user to create conf file in user home. 
# Rerun setup: run with --setup
# Dependencies: python python-requests
#
# Note: Uses one system wide api_token only. Not meant for multi-user environments.
# Note: There's no stopping anyone from adding this bot to their Telegram. 
#       The messages will however only go to the chat_id in the config file
# Note: You can store a system wide config file as /etc/telegrambot.conf 
#       this will be used if the user has read permissions for it and no ~/.telegrambot.conf is found.
#		Use this for root or www-data, but be sure to deny read for everyone else.
#
# USAGE: telegrambot.py "MESSAGE" "LOCAL IMAGE (optional)"
# (MESSAGE supports markdown) 
#
# Fredrik Welander 2016
#

import os
import subprocess
import sys
import socket
#import ConfigParser
import configparser
# request seems not to be installed by default on Debian/Ubuntu, check for it
try:
	import requests
except ImportError:
	print("Unmet dependencies. Install python3-requests")
	exit(1)

usage = 'USAGE: telegrambot.py [--setup] "MESSAGE" "LOCAL IMAGE (optional)"'
hostname = socket.gethostbyaddr(socket.gethostname())[0]

# Init config
config = configparser.ConfigParser()   
configFileUser = "{}/.telegrambot.conf".format(os.path.expanduser("~") )
configFileGlobal = "/etc/telegrambot.conf"


# Request function
def botcall(method, token, params={}, photo={}):
	url = "https://api.telegram.org/bot{0}/{1}".format(token, method)
	#print("{} params:{}".format(url, str(params)))
	response = requests.post(
		url=url,
		params=params,
		files=photo
	).json()
	if not response["ok"]:
		print("Telegrambot request error: {0} {1}".format(response["error_code"], response["description"]))
		exit(1)
	return response

# Read possible config_files, configFileUser overrides if present
read_config = config.read([configFileGlobal, configFileUser])

if not read_config or (len(sys.argv) == 2 and sys.argv[1] == "--setup"):

	# Set user config file as configFile
	configFile = configFileUser

	if input("Run setup? [Y/n]: ").lower() not in [ 'y', '' ]:
		exit(0)
	
	token = input("Enter Telegram Bot API token: ").strip()
	bot_uname = botcall("getMe", token)["result"]["username"]
	print("Bot {0} found. Getting last chat_id...".format(bot_uname))

	if not config.has_section('main'):
		config.add_section('main')
	config.set('main', 'api_token', token)
	config.set('main', 'bot', bot_uname)

	# Request: get chats for bot
	chats = botcall("getUpdates", token)["result"]

	if len(chats) == 0:
		print("No recent chats found for bot {}. Send a message to it in Telegram so you get a chat_id, then re-run Setup.".format(bot_uname))
		exit(1)

	# Get last chat id
	last_chat = chats[-1]["message"]["chat"]
	if input("Found chat_id {0} for user {1} {2}. Is this correct? [Y/n]: "
		.format(
			last_chat["id"], 
			last_chat["first_name"], 
			last_chat["last_name"])).lower() not in [ 'y', '' ]:
		exit(0)
	config.set('main', 'chat_id', str(last_chat["id"]))

	# Write to config file
	cfgfile = open(configFile,'w')
	config.write(cfgfile)
	cfgfile.close()
	#os.chmod(configFile, "o-r")
	subprocess.call(["chmod", "o-r", configFile])

	print("Config file {} created.".format(configFile))
	print("Setup complete.")
	print(usage)
	exit(0)

# Check for correct amount of args
if len(sys.argv) < 2:
	print(usage)
	sys.exit(1)

# Read api token from config
token = config.get('main', 'api_token')
chat_id = config.get('main', 'chat_id')
message = "[{0}]: {1}".format(hostname, sys.argv[1])

# Check for possible photo
if (len(sys.argv) == 3 
	and os.path.isfile(sys.argv[2]) 
	and sys.argv[2].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))):
	
	photo = open(sys.argv[2], 'rb')
	botcall("sendPhoto", token, { "chat_id": chat_id, "caption": message} , { "photo": photo })
else:
	# Send message
	botcall("sendMessage", token, { "chat_id": chat_id, "text": message })



