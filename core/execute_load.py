#!/usr/bin/env python3
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/storage")
sys.path.append(user_home + r"/automatic-octopus/core/message")
from load_tracks import tracks_to_pg#pylint: disable=import-error
from transmit import communicado#pylint: disable=import-error

#Get the environment variables needed to load the data
sheet_name = os.getenv("response_sheet")

# Load the tables and send a text message if it fails
success =tracks_to_pg()
communicado(success)