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
Common Utilities Module contains functions such as to update file according to regex, logging etc
'''

import os, re, sys, shutil
import tempfile, logging
from custom_modules import Directory_utilities

properties = {}

####-----Function to read properties from input file to dictionary-----####
def set_properties_dict(properties_file):
    logging.info('----Inside function read_properties()----')
    logging.info('Reading properties file: {}'.format(properties_file))
    myvars = {}
    with open(properties_file) as dfile:
        for line in dfile:
            if '=' in line and line[0] != '#':
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = var
    global properties
    properties = myvars
    return myvars

####-----Function to update the file contents matching the given regex-----####
def update_file(filename, regex_pattern, replacewith):
    logging.info('----Inside function update_file()----')
    ####   Creating temp file for edit   ####
    tempdir = get_tempdir()
    tmpfd, tmpfile = tempfile.mkstemp(dir=tempdir)
    logging.debug('Creating temp file {}...'.format(tmpfile))
    logging.info('Updating value for regex: {} in file: {} with value: {}'.format(regex_pattern, filename, replacewith))
    os.close(tmpfd)

    regex_searched = False
    
    with open(filename, 'r', encoding='utf-8') as infile:
        with open(tmpfile, 'w', encoding='utf-8') as ofile:
            for line in infile:
                try:
                    searchObj = re.search(regex_pattern, line)
                    if searchObj is not None:
                        replace_obj = searchObj.group(1)
                        newline = line.replace(replace_obj, replacewith)
                        ofile.write(newline)
                        regex_searched = True
                        logging.info('Regex matched : {}'.format(replace_obj))
                    else:
                        ofile.write(line)
                except AttributeError as err:
                    logging.error('File: {} failed to update due to error: {}!'.format(filename, err))
                    logging.debug('Deleting temp file {}...'.format(tmpfile))
                    print('File: {} failed to update due to error: {}!'.format(filename, err))
                    ofile.close()
                    os.remove(tmpfile)
                    sys.exit(err)

    if not regex_searched:
        logging.error('Search pattern not found')
        return False
    
    ####   Replacing file with new file   ####
    logging.debug('Replacing temp file {}...'.format(tmpfile))
    os.remove(filename)
    os.rename(tmpfile, filename)
    return True

####-----Function to read property value-----####
def read_property(property_key, required = True):
    logging.info('----Inside function read_property()----')
    logging.info('Reading property key: {}'.format(property_key))
    try:
        val = properties[property_key].strip()
        if val == '' and required == true:
            exit('Value for required property {} cannot be blank'.format(property_key))
        return val
    except Exception:
        if required == False:
            return ''
        else:
            exit('Value for required property {} not found'.format(property_key))

####-----Function to convert string to boolean-----####
def str_to_bool(s):
    if s.strip().lower() == 'true':
        return True
    elif s == 'false':
        return False
    else:
        exit('Invalid value: {}'.format(s))

####-----Function to exit with error-----####
def exit(msg='', tempdir=None):
    print(msg)
    if tempdir:
        logging.debug('Deleting temp folder {}...'.format(tempdir))
        shutil.rmtree(tempdir)
    logging.error('Exiting the installer...\n')
    sys.exit('Exiting the installer...\n')

####-----Function to create uri from parts-----####
def getUri(host, port=None, path=''):
    if port:
        return '{}:{}/{}'.format(host, port, path)
    else:
        return '{}/{}'.format(host, path)

####-----Function to add property-----####
def add_property(key, val):
    global properties
    properties[key] = val

####-----Function to get temp folder-----####
def get_tempdir():
    installer_tempdir = tempfile.gettempdir()
    tempdir = os.path.join(installer_tempdir, 'DSCS_Installer')
    Directory_utilities.create_folder(tempdir)
    logging.debug('Creating temp folder {}...'.format(tempdir))
    return tempdir

####-----Function to get script usage-----####
def get_usage(exitCode=None):
    print("Usage: Installer.py -c <component(server/console)> -i <inputpath> -p <propertiespath>")
    sys.exit(exitCode)