#!/usr/bin/python3

# Easily send emails with attachments from cron
# 
# Mostly stolen from gist https://gist.github.com/srv89/1d3dac6672895f5ca65f
#
# Usage (required params):    sendmail.py to=[to_addr] subject="Subject"
# Usage (all possible params: sendmail.py to="to_addr[,to_addr...]" subject="Subject" body="Message body" attach=path/to/folder/|/path/to/file.ext
#
# Attach can be one of the following:
# /path/to/folder/ # will attach everything from this folder (end with /)
# /path/to/file.ext # will attach only thif file

import os, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json

conf_file = "/etc/sendmail_py.json"
# Conf file example, remember to chmod correctly!
#
# { 
#   "comment": "Conf file for misc-scripts-sendmail.py",
#   "server": "outlook.office365.com",
#   "port" :587,
#   "username" : "some.user@somedomain.fi",
#   "password" : "MyPassword123"
# }
#

if len(sys.argv) < 2:
    sys.exit('USAGE: sendmail.py to=to_addr subject="Subject" [ from=from_addr body="Message body" attach=path/to/folder/|/path/to/file.ext ]')

params = {}
for arg in sys.argv[1:]:
    params[arg.split("=")[0]] = arg.split("=")[1]

try:
    with open(conf_file) as json_data_file:
        conf = json.load(json_data_file)
except:
    sys.exit("Unable to read conf file {}".format(conf_file))

smtp_server = conf['server']
smtp_port = conf['port']
username = conf['username']  # Email Address from the email you want to send an email
password = conf['password']  # Password


from_addr = params['from'] if 'from' in params else username
email_list = params['to'].split(',')
subj = params['subject']
html = params['body'] if 'body' in params else subj
attach = params['attach'] if 'attach' in params else None



# Create the body of the message (a HTML version for formatting).
#html = """Add you email body here"""

# Function that send email.
server = smtplib.SMTP('')
def send_mail(username, password, from_addr, to_addrs, msg):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()

# Read email list txt
#email_list = [line.strip() for line in open('email.txt')]

for to_addrs in email_list:
    msg = MIMEMultipart()

    msg['Subject'] = subj
    msg['From'] = from_addr
    msg['To'] = to_addrs

    # Attach HTML to the email
    body = MIMEText(html, 'html')
    msg.attach(body)

    # Attach Cover Letter to the email
    if attach is not None:
        file_list = []
        if attach.strip()[-1] == "/":
            try:
                for filename in os.listdir(attach):
                    file_list.append(attach.strip()+filename)
            except:
                sys.exit("Attachment directory {} not found.".format(attach))
        else:
            file_list = [ attach ]

        if len(file_list) == 0:
            sys.exit("No attachments found in directory")

        #sys.exit(file_list.count())

        for file in file_list:
            try:
                open(file)
            except:
                sys.exit("Attachment file {} not found.".format(file))

            cover_letter = MIMEApplication(open(file, "rb").read())
            cover_letter.add_header('Content-Disposition', 'attachment', filename=file.split("/")[-1])
            msg.attach(cover_letter)

    try:
        send_mail(username, password, from_addr, to_addrs, msg)
        print("Email successfully sent to", to_addrs)
    except SMTPAuthenticationError:
        print('SMTPAuthenticationError')
        print("Email not sent to", to_addrs)