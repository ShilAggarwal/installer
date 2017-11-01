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
Deployment Module is for deploying war and dist to jboss and apache respectively
'''
import os, shutil
import logging, time
from time import sleep
from custom_modules import Common_utilities, Directory_utilities

####-----Function to handle scenario where war with same name already exist in jboss-----####
def duplicate_war(warfile):
    logging.info('----Inside function duplicate_war()----')
    
    ####   WAR deployment status   ####
    war_deployed = warfile+'.deployed'
    war_undeployed = warfile+'.deployed'
    war_failed = warfile+'.failed'

    try:        
        if os.path.exists(warfile):
            logging.debug('Duplicate warfile exists: {}'.format(warfile))
            Directory_utilities.delete_file(warfile, True)
            sleep(5)
            Directory_utilities.delete_file(war_failed, True)
            timeout = time.time() + 5
            while not os.path.exists(war_undeployed) and time.time() < timeout:
                print('!.!.!.!.!.!.!.!.!.!.!.!.!.!.!.!')
                sleep(2)
            Directory_utilities.delete_file(war_undeployed, True)
        return True

    except Exception as err:
        logging.error('JBOSS deployment failed with error: {}'.format(err))
        return False   

####-----Function to deploy war file in standalone mode-----####
def jboss_deploy(warfile):
    logging.info('----Inside function jboss_deploy()----')
    deployment_mode = Common_utilities.read_property('installer.jboss.mode')
    logging.debug('deployment mode is: {}'.format(deployment_mode))
    print('Deployment mode is: {}'.format(deployment_mode))
       
    ####   Copy to jboss deployment in case of single-server mode   ####
    if deployment_mode == 'standalone':
        print('Deploying WAR to JBOSS...')
        deployment_path = os.path.abspath(Common_utilities.read_property('installer.jboss.path'))
        
        if not os.path.exists(deployment_path):
            Common_utilities.exit('Invalid jboss path!')
        
        logging.debug('JBOSS deployment path: {}'.format(deployment_path))
        logging.debug('Copying WAR to JBOSS deployment folder {}'.format(deployment_path))
        new_warfile = os.path.join(deployment_path, os.path.basename(warfile))

        ####   Remove the duplicate war   ####
        logging.debug('')
        result = duplicate_war(new_warfile)

        if not result:
            Common_utilities.exit('JBOSS deployment failed.')

        ####   Copy war to jboss   ####
        try:
            shutil.copy(warfile, deployment_path)
        except Exception as err:
            Common_utilities.exit('JBOSS deployment failed with error: {}'.format(err))

        ####   Check if deployed successfully   ####
        war_deployed = new_warfile+'.deployed'
        war_undeployed = new_warfile+'.deployed'
        war_failed = new_warfile+'.failed'

        ####    Set timeout for deployment as 2 minutes    ####
        timeout = time.time() + 60*2

        while not(os.path.exists(war_deployed) or os.path.exists(war_undeployed) or os.path.exists(war_failed)) and time.time() < timeout:
            sleep(2)
            print('!.!.!.!.!.!.!.!.!.!.!.!.!.!.!.!')
        
        if os.path.exists(war_deployed):
            logging.info('WAR deployed successfully !\n')
            print('War deployed successfully!\n')
            return True
        else:
            logging.error('JBOSS deployment failed.')
            print('War deployment failed! Check JBOSS logs')
            return False
    elif deployment_mode == 'cluster':
        out_dir = os.path.join(os.getcwd(), 'out')
        print('Updated WAR file is placed at output folder: {}. Please refer to section 5.2 in \"Installation Guide.pdf\" for detailed deployment steps.\n'.format(out_dir))
    else:
        Common_utilities.exit('Invalid jboss mode. Value can be either \'cluster\' or \'standalone\'')
        

####-----Function to deploy war file-----####
def apache_deploy(distfolder):
    logging.info('----Inside function apache_deploy()----')
    deployment_path = os.path.abspath(Common_utilities.read_property('installer.apache.path'))
    if not os.path.exists(deployment_path):
        Common_utilities.exit('Invalid apache path!')
    try:
        apache_context = Common_utilities.read_property('installer.apache.context')
        apache_context_path = os.path.join(deployment_path, apache_context)
        logging.debug('Deploying folder to Apache folder: {}'.format(deployment_path))

        Directory_utilities.copy_folder_contents(distfolder, apache_context_path)

        print('Folder deployed to apache successfully!')
        logging.info('Deployment successful !\n')
    except Exception as err:
        Common_utilities.exit('Error with apache deployment: {}'.format(err))
