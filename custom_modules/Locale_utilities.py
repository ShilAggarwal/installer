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
Locale_utilities Module for locale specific methods
'''
import logging
from custom_modules import Common_utilities

locales_list = ['en_us', 'ja_jp']

####-----Function to validate locale-----####
def validate_locale():
    logging.info('----Inside function validate_locale()----')
    logging.info('Reading locales properties')
    locale_properties_list = get_locale_properties()
    ####   Validate all locale properties    ####
    for locale_property in locale_properties_list:
        if(locale_property.lower() not in locales_list):
            logging.error('{} is not a valid locale'.format(locale_property))
            print('{} is not a valid locale'.format(locale_property))
            print('Allowed values for locales are: {}'.format(locales_list))
            return False
    return True

####-----Function to get locale properties-----####
def get_locale_properties():
    logging.info('----Inside function gete_locale_properties()----')
    logging.info('Reading locales properties')
    locale_properties_list = []
    ####   Add all locale properties    ####
    locale_properties_list.append(Common_utilities.read_property('email.properties.signup.locale'))
    locale_properties_list.append(Common_utilities.read_property('email.properties.resetpassword.locale'))
    locale_properties_list.append(Common_utilities.read_property('email.properties.license.locale'))
    return locale_properties_list