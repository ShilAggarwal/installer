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
Classes required for the installer
'''

####-----Server Class-----####
class Server:
    host = ''
    port = ''
    isAuthenticated = False
    username = None
    password = None

class Smtp_server(Server):
    def __init__(self, host, port, isAuthenticated, username=None, password=None):
        self.host = host
        self.port = port
        self.isAuthenticated = isAuthenticated

        if isAuthenticated:
            if username:
                self.username = username
            if password:
                self.password = password
