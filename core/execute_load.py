#This script will pull the API data and load the tables. Eventually, a message
#should be added that provides updates if the run fails

# Import libraries
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automaton/core/storage")
from load_tables import extract_load#pylint: disable=import-error

extract_load()