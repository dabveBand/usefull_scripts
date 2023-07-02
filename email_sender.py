#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# description   : send email with Gmail 2023; NOTE: your to create an app in Gmail
# ---------------------------------------------------------------------------------
from email.message import EmailMessage
import ssl
import smtplib
from getpass import getpass


def send_email(sender, receiver, subject, body):
    pwd = getpass('[?] Gmail Password: ')
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()                  # connect over SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        # 'smtp.gmail.com:465'
        smtp.login(sender, pwd)                             # login to Gmail sender
        smtp.sendmail(sender, receiver, em.as_string())     # send the message


if __name__ == '__main__':
    sender = 'bdabve@gmail.com'
    receiver = 'bdabve@gmail.com'
    subject = 'Test email sending with python'
    body = 'Testing gmail with the new version of enabling password in gmail/apppasswprds'
    send_email(sender, receiver, subject, body)
