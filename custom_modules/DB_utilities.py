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
DB_utilities Module for mongo and AEM DB (mysql/mssql) connectivity
'''

from pymongo import MongoClient, errors
import mysql.connector
from  mysql.connector import connection, errorcode
import logging
from custom_modules import Common_utilities
import pyodbc


####-----Function to verify MongoDB connection-----####
def verify_mongo(uri):
    logging.info('----Inside function verify_mongo()----')
    maxSevSelDelay = 1
    print('Verifying Mongo DB connection...')

    ####   Test MongoDB connection   ####
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        logging.debug('Mongo DB connected')
        print('Mongo DB connected')
        return True

    ####   Error handling   ####
    except errors.ServerSelectionTimeoutError as err:
        logging.error('Mongo DB connection failed with error: {}'.format(err))
        print('Mongo DB connection failed with error: {}'.format(err))
        return False
    except errors.InvalidURI as err:
        logging.error('Invalid mongo db uri: {}'.format(err))
        print('Invalid mongo db uri: {}'.format(err))
        return False
    except Exception as err:
        logging.error('Mongo DB connection failed with error: {}'.format(err))
        print('Mongo DB connection failed with error: {}'.format(err))
        return False


####-----Function to verify sql connection-----####
def verify_aemDB(properties):
    logging.info('----Inside function verify_aemDB()----')

    ####   Read database properties   ####
    logging.info('Reading AEM DB properties')
    sql_hostname = Common_utilities.read_property('installer.datasource.hostname')
    sql_port = Common_utilities.read_property('installer.datasource.port')
    sql_database = Common_utilities.read_property('installer.datasource.database')
    aemdb_authenticated = Common_utilities.read_property('installer.datasource.authenticated')

    # change string to boolean
    aemdb_authenticated = Common_utilities.str_to_bool(aemdb_authenticated)

    ####   Read database username and password   ####
    if aemdb_authenticated:
        logging.info('Reading AEM database username and password')
        sql_username = Common_utilities.read_property('spring.datasource.username')
        sql_password = Common_utilities.read_property('spring.datasource.password')

    ####   Check whether the database is mysql or mssql
    database = Common_utilities.read_property('database-id')
    logging.info('Database id is {}'.format(database))

    ####   Construct jdbc connection string
    if database == 'mysql':
        jdbc_str = 'jdbc:mysql://{}:{}/{}\n'.format(sql_hostname, sql_port, sql_database)
        jdbc_driver = 'com.mysql.cj.jdbc.Driver\n'
    elif database == 'mssqlserver':
        jdbc_str = 'jdbc:sqlserver://{}:{};database={}\n'.format(sql_hostname, sql_port, sql_database)
        jdbc_driver = 'com.microsoft.sqlserver.jdbc.SQLServerDriver\n'
    else:
        ####   Invalid value of database-id
        logging.error('Invalid value of database-id. Value can be either mysql or mssqlserver !')
        print('Invalid value of database-id. Value can be either mysql or mssqlserver !')
        return False

    logging.debug('JDBC connection string is: {}'.format(jdbc_str))

    ####   Set additional aem db properties   ####
    Common_utilities.add_property('spring.datasource.url', jdbc_str)
    Common_utilities.add_property('spring.datasource.driver-class-name', jdbc_driver)
    Common_utilities.add_property('mybatis.configuration.database-id', Common_utilities.read_property('database-id'))

    ####   Test mssql connection   ####
    driver = '{ODBC Driver 13 for SQL Server}'
    if database == 'mssqlserver':
        print('Verifying mssql connection...')
        try:
            if aemdb_authenticated:
                connStr = 'DRIVER=' + driver + ';SERVER=' + sql_hostname + ',' + sql_port + ';DATABASE=' + sql_database + ';UID=' + sql_username + ';PWD=' + sql_password
                logging.info('mssql connection string: {}'.format(connStr))
            else:
                connStr = 'DRIVER=' + driver + ';SERVER=' + sql_hostname + ',' + sql_port + ';DATABASE=' + sql_database
                logging.info('mssql connection string: {}'.format(connStr))

            conn = pyodbc.connect(connStr)
            logging.info('mssql connected')
            print("mssql connected")

            ####   Error handling   ####
        except Exception as err:
            logging.error("mssql connection failed with error: {}".format(err))
            print("mssql connection failed with error: {}".format(err))
            return False

        ####   Close connection   ####
        else:
            logging.debug('Closing mssql connection')
            conn.close()
            return True

    ####   Test mysql connection   ####
    elif database == 'mysql':
        print('Verifying mysql connection...')
        try:
            if aemdb_authenticated:
                conn = connection.MySQLConnection(host=sql_hostname, user=sql_username, passwd=sql_password,
                                                  database=sql_database, port=sql_port)
            else:
                conn = connection.MySQLConnection(host=sql_hostname, database=sql_database, port=sql_port)

            logging.debug('Connection string for mysql = {}'.format(conn))
            logging.info('mysql connected')
            print('mysql connected')

        ####   Error handling   ####
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error('mysql connection failed with error: Invalid user name or password !')
                print('mysql connection failed with error: Invalid user name or password !')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error('mysql connection failed with error: Database does not exist !')
                print('mysql connection failed with error: Database does not exist !')
            else:
                logging.error('mysql connection failed with error: {}'.format(err))
                print(err)
            return False

        ####   Close connection   ####
        else:
            logging.debug('Closing myssql connection')
            conn.close()
            return True

    return True
