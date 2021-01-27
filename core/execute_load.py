#!/usr/bin/env python3
#pylint: disable=import-error
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/storage")
sys.path.append(user_home + r"/automatic-octopus/core/message")
from load_tracks import tracks_to_pg
from load_responses import responses_to_pg
from transmit import communicado

#Get the environment variables needed to load the data
sheet_name = os.getenv("response_sheet")

# Load the tables and send a text message if it fails
track_success = tracks_to_pg()
response_success = responses_to_pg(sheet_name)

if track_success is False or response_success is False:
    communicado(False)
else:
    print('Everything is great!')
