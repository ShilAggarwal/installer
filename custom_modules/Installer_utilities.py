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
Installer_utilities Module for installer specific methods
'''

import logging
import re
import os
from custom_modules import Common_utilities, Classes

mainjs_file = ''
index_html_file = ''
htaccess_file = ''

####-----Function to validate console folder-----####
def validate_console(console_path):
    global mainjs_file
    global index_html_file
    global htaccess_file

    ####   Search for the main.*.js file   ####
    mainjs_regex = re.compile(r'main\.(.*)\.bundle\.js$')
    mainjs_found = False
    for file in os.listdir(console_path):
        if mainjs_regex.match(str(file)):
            mainjs = file
            logging.debug('Found {}'.format(mainjs))
            mainjs_found = True

    ####   Check if main.js file found   ####
    if not mainjs_found:
        Common_utilities.exit('main.*.bundle.js file required for console configuration not found!')

    mainjs_file = os.path.join(console_path, mainjs)

    ####   Check if index.html exists   ####
    index_html_file = os.path.join(console_path, 'index.html')
    if not os.path.exists(index_html_file):
        Common_utilities.exit('index.html file required for console configuration not found!')

    ####   Check if .htaccess exists   ####
    htaccess_file = os.path.join(console_path, '.htaccess')
    if not os.path.exists(htaccess_file):
        Common_utilities.exit('.htaccess file required for console configuration not found!')

####-----Function to process console deployment-----####
def update_console(console_path, server_path, context_path):
    print('Updating the main.*.bundle.js file')
    ret_val = True
    basepath_regex = r'"app.config".*?basePath:"(.*?)"'
    result = Common_utilities.update_file(mainjs_file, basepath_regex, server_path)

    if not result:
        ret_val = False
        logging.error('main.*.bundle.js failed to update !')
        print('main.*.bundle.js failed to update !')

    ####   Update the index.html file   ####
    print('Updating the index.html file')
    contextpath_regex = r'<base href="/(.*?)/"'
    result = Common_utilities.update_file(index_html_file, contextpath_regex, context_path)

    if not result:
        ret_val = False
        logging.error('index.html failed to update !')
        print('index.html failed to update !')

    ####   Update the .htaccess file   ####
    print('Updating the .htaccess file')
    basepath_regex = r'RewriteBase /(.*?)/'
    result1 = Common_utilities.update_file(htaccess_file, basepath_regex, context_path)
    redirectionrule_regex = r'RewriteRule . /(.*?)/'
    result2 = Common_utilities.update_file(htaccess_file, redirectionrule_regex, context_path)

    if not result1 or not result2:
        ret_val = False
        logging.error('.htaccess failed to update !')
        print('.htaccess failed to update !')
    
    return ret_val

####-----Function to process SMTP properties-----####
def process_smtp_properties():
    logging.info('----Inside function process_smtp_properties()----')
    logging.info('Reading SMTP server properties')
    Common_utilities.add_property('spring.mail.properties.mail.smtp.starttls.enable', 'true\n')
    smtp_host = Common_utilities.read_property('spring.mail.host')
    smtp_port = Common_utilities.read_property('spring.mail.port')
    smtp_isAuthenticated = Common_utilities.read_property('installer.smtp.authenticated')
    smtp_isAuthenticated = Common_utilities.str_to_bool(smtp_isAuthenticated)

    smtp_obj = Classes.Smtp_server(smtp_host, smtp_port, smtp_isAuthenticated)

    ####   Read username and password if smtp is authenticated   ####
    if smtp_isAuthenticated:
        logging.info('Reading SMTP server username and password')
        smtp_username = Common_utilities.read_property('spring.mail.username')
        smtp_password = Common_utilities.read_property('spring.mail.password')
        Common_utilities.add_property('spring.mail.properties.mail.smtp.auth', 'true\n')
        smtp_obj.username = smtp_username
        smtp_obj.password = smtp_password

    return smtp_obj

####-----Function to process MongoDB properties-----####
def process_mongodb_properties():
    logging.info('----Inside function process_mongodb_properties()----')
    logging.info('Reading mongodb server properties')
    Common_utilities.add_property('spring.data.mongodb.repositories.enabled', 'true\n')
    mongodb_uri = Common_utilities.read_property('spring.data.mongodb.uri', False)

    ####   Mongo DB properties if mongo uri not provided   ####
    if mongodb_uri == '':
    ####   Mongo DB properties for authenticated server   ####
        mongodb_uri = construct_mongo_uri()
    else:
        mongo_server = Common_utilities.read_property('spring.data.mongodb.host', False)
        mongo_port = Common_utilities.read_property('spring.data.mongodb.port', False)
        mongo_database = Common_utilities.read_property('spring.data.mongodb.database', False)
        mongodb_username = Common_utilities.read_property('spring.data.mongodb.username', False)
        mongodb_password = Common_utilities.read_property('spring.data.mongodb.password', False)

        if mongo_server != '' or mongo_port != '' or mongo_database != '' or mongodb_username != '' or mongodb_password != '':
            Common_utilities.exit('Either mongo uri or other mongo properties should be provided')
    return mongodb_uri

####-----Function to construct MongoDB uri-----####
def construct_mongo_uri():
    logging.info('----Inside function construct_mongo_uri()----')
    ####   Read mongo properties from dictionary   ####
    logging.info('Reading Mongo DB properties')
    mongo_server = Common_utilities.read_property('spring.data.mongodb.host')
    mongo_port = Common_utilities.read_property('spring.data.mongodb.port')
    mongo_database = Common_utilities.read_property('spring.data.mongodb.database')
    mongodb_authenticated = Common_utilities.read_property('installer.mongodb.authenticated')

    ####   change string to boolean    ####
    mongodb_authenticated = Common_utilities.str_to_bool(mongodb_authenticated)

    ####   Read username and password if mongo db is authenticated   ####
    if mongodb_authenticated:
        logging.info('Reading Mongo DB username and password')
        mongo_username = Common_utilities.read_property('spring.data.mongodb.username')
        mongo_password = Common_utilities.read_property('spring.data.mongodb.password')
        uri = 'mongodb://{}:{}@{}:{}/{}'.format(mongo_username, mongo_password, mongo_server, mongo_port, \
                                                mongo_database)

    else:
        uri = 'mongodb://{}:{}'.format(mongo_server, mongo_port)
    logging.debug('Connection string for mongo = {}'.format(uri))
    return uri

####-----Function to process sign-up properties-----####
def process_signup_properties():
    logging.info('----Inside function process_signup_properties()----')
    signup_registration_mail_from = Common_utilities.read_property('email.properties.signup.registrationMailFrom')
    signup_activation_mail_from = Common_utilities.read_property('email.properties.signup.activationMailFrom')
    signup_mail_locale = Common_utilities.read_property('email.properties.signup.locale')

####-----Function to process reset password properties-----####
def process_reset_password_properties():
    logging.info('----Inside function process_reset_password_properties()----')
    reset_password_mail_from = Common_utilities.read_property('email.properties.resetpassword.mailFrom')
    reset_password_mail_locale = Common_utilities.read_property('email.properties.resetpassword.locale')

####-----Function to process licensing properties-----####
def process_licensing_properties():
    logging.info('----Inside function process_licensing_properties()----')
    licensing_mail_to = Common_utilities.read_property('email.properties.license.mailTo')
    licensing_mail_from = Common_utilities.read_property('email.properties.license.mailFrom')
    licensing_mail_locale = Common_utilities.read_property('email.properties.license.locale')

####-----Function to process System manager properties-----####
def process_sysmgr_properties():
    logging.info('----Inside function process_sysmgr_properties()----')
    sysmgr_username = Common_utilities.read_property('sysmgr.context.username')
    sysmgr_password = Common_utilities.read_property('sysmgr.context.password')
    
