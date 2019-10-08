#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# import necessary packages
# 
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import smtplib
import argparse
# 
# create message object instance
msg = MIMEMultipart()
message = "Thank you       "
#
# Proc args
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="User: ")
parser.add_argument("-p", "--pwd", help="Password: ")
parser.add_argument("-t", "--to", help="To: ")
parser.add_argument("-s", "--subject", help="Subject: ")
parser.add_argument("-m", "--message", help="Message: ")
parser.add_argument("-a", "--attach", help="Attach: ")
args = parser.parse_args()
#
falta=0
if not args.user:
    print "mail.py: Falta usuario"
    falta=1
if not args.pwd:
    print "mail.py: Falta password"
    falta=1
if not args.to:
    print "mail.py: Falta destinatario"
    falta=1
if not args.subject:
    print "mail.py: Falta subject"
    falta=1
if not args.message:
    print "mail.py: Falta mensaje"
    falta=1
if falta == 1:
    quit()
#
#if args.attach:
#    print "El archivo a enviar es: ", args.attach
#
# setup the parameters of the message
#password = "SapHelp.18"
#msg['From'] = "alertas@saphelp.cl"
#msg['To'] = "tomas@aservices.cl"
#msg['Subject'] = "Prueba iops"
#message = "Thank you       "
#textfile = "iops-nbwprdnwsav-20181025-170725.txt"
password = args.pwd
msg['From'] = args.user
msg['To'] = args.to
msg['Subject'] = args.subject
message = args.message
textfile = args.attach
#
# add in the message body
msg.attach(MIMEText(message, 'plain'))
#
# attach text file
if args.attach:
    f = file(textfile)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename = textfile)
    msg.attach(attachment)
#
# attach image to message body
#msg.attach(MIMEImage(file("google.jpg").read()))
#
#create server
server = smtplib.SMTP('smtp.zoho.com: 587')
server.starttls()
#
# Login Credentials for sending the mail
server.login(msg['From'], password)
#
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()
print "mail.py: successfully sent email to %s:" % (msg['To'])
#
