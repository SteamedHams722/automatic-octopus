#!/usr/bin/env python3
#pylint: disable=import-error
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
from datetime import datetime
from time import sleep
import logging
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/storage")
sys.path.append(user_home + r"/automatic-octopus/core/message")
from load_tracks import tracks_to_pg, analysis_to_pg
from load_responses import responses_to_pg
from transmit import communicado

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

#Get the environment variables needed to load the data
sheet_name = os.getenv("response_sheet")

# Load the tables and send a text message if it fails
track_success = tracks_to_pg()
response_success = responses_to_pg(sheet_name)
sleep(60) #Making the app sleep before it executes the analysis function
analysis_success = analysis_to_pg()
success_dict = {'tracks': track_success, 'responses': response_success, 'analysis': analysis_success}

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