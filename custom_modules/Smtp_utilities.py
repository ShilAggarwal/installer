'''/*
 * ***********************************************************************
 *   ADOBE CONFIDENTIAL
 *   _________________________
 *   Copyright 2016 Adobe Systems Incorporated
 *   All Rights Reserved.
 *
 *  NOTICE:  All information contained herein is, and remains
 *  the property of Adobe Systems Incorporated and its suppliers,
 *  if any.  The intellectual and technical concepts contained
 *  herein are proprietary to Adobe Systems Incorporated and its
 *  suppliers and are protected by all applicable intellectual property
 *  laws, including trade secret and copyright laws.
 *  Dissemination of this information or reproduction of this material
 *  is strictly forbidden unless prior written permission is obtained
 *  from Adobe Systems Incorporated.
 *  ************************************************************************
 */

Description:
============
Smtp_utilities Module for smtp connectivity
'''

import logging
import smtplib
from email.mime.text import MIMEText
from custom_modules import Common_utilities, Classes

####-----Function to verify smtp connection-----####
def verify_smtp(smtp_server):
    logging.info('----Inside function verify_smtp()----')

    ####    If smtp server is authenticated    ####
    if smtp_server.isAuthenticated:
        result = send_test_mail(smtp_server.host, smtp_server.port, smtp_server.username, smtp_server.password)

    else:
        result = send_test_mail(smtp_server.host, smtp_server.port)

    return result

def send_test_mail(host, port, username=None, password=None):
    logging.info('----Inside function send_test_mail()----')
    msg = MIMEText("Test")

    ####    Set sender and recipients mail    ####
    sender = "test@from.com"
    recipient = "test@to.com"

    ####    Other mail parts    ####
    msg['Subject'] = 'Test'
    msg['From'] = sender
    msg['To'] = recipient

    server = None
    try:
        server = smtplib.SMTP(host, port)
        if username and password:
            server.login(username, password)
        server.sendmail(sender, [recipient], msg.as_string())
        logging.error('SMTP connection successful')
        print('SMTP connection successful')
        return True

    except Exception as err:
        logging.error('SMTP connection failed with error: {}'.format(err))
        print('SMTP connection failed with error: {}'.format(err))
        return False

    else:
        logging.info('Closing smtp connection...')
        server.quit()