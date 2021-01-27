#!/usr/bin/env python3
#pylint: disable=import-error
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
from datetime import datetime
import logging
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/storage")
sys.path.append(user_home + r"/automatic-octopus/core/message")
from load_tracks import tracks_to_pg
from load_responses import responses_to_pg
from transmit import communicado

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

#Get the environment variables needed to load the data
sheet_name = os.getenv("response_sheet")

# Load the tables and send a text message if it fails
track_success = tracks_to_pg()
response_success = responses_to_pg(sheet_name)

if track_success is False or response_success is False:
    communicado(False)
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f" {timestamp} Failure message sent. There was an issue when trying to load data"
    logging.info(message)
else:
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f" {timestamp} No message sent. Both jobs succeeded."
    logging.info(message)
