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
File_utilities Module for directory/file related functions
'''

import os
import logging
import shutil

####-----Function to create a directory-----####
def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

####-----Function to delete a directory-----####
def delete_folder(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

####-----Function to delete a file-----####
def delete_file(filename, log = False):
    if os.path.exists(filename):
        if(log):
            logging.debug('Removing {}'.format(filename))
        os.remove(filename)

####-----Function to copy all contents of src folder to dst folder-----####
def copy_folder_contents(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)