#!/usr/bin/env python3
#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/storage")
sys.path.append(user_home + r"/automatic-octopus/core/message")
from load_tables import extract_load#pylint: disable=import-error
from transmit import communicado#pylint: disable=import-error

# Load the tables and send a text message if it was successful
success = extract_load()
communicado(success)
