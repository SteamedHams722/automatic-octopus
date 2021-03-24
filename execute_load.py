#!/usr/bin/env python3
#pylint: disable=import-error
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
from datetime import datetime
import logging
user_home = os.path.expanduser("~")
sys.path.append(os.path.join(user_home, 'core', 'storage'))
sys.path.append(os.path.join(user_home, 'core', 'message'))
from load_tracks import tracks_to_pg
from load_responses import responses_to_pg
from transmit import communicado

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

def load_all():
    '''Need to have a function here so Heroku can call it. I'm currently excluding the
    response calls since it is not working correctly on raspberry pi.'''

    # Load the tables and send a text message if it fails
    success_dict = {'tracks': tracks_to_pg(), 'responses': responses_to_pg(os.getenv('response_sheet'))}

    #TODO: Add responses function call and add the results to a success dictionary
    # with the track_success data

    for key, val in success_dict.items():
        if val: # A True value means the job succeeded.
            #communicado(table_group=key, success=val) #This is only needed for testing.
            timestamp = datetime.utcnow().replace(microsecond=0)
            message = f" {timestamp} No message sent. Data load jobs succeeded."
        else:
            communicado(table_group=key, success=val)
            timestamp = datetime.utcnow().replace(microsecond=0)
            message = f" {timestamp} Failure message sent. There was an issue when trying to load data"
            logging.info(message)