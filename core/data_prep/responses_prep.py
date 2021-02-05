# This script will provide a function that takes the data provided by the csv document
# and turns it into a json file that can be loaded into postgres. Using json is
# a cleaner and more flexible way to load and transform the data.

# Load libraries
import os
import sys
import numpy as np
from datetime import datetime, timezone
import logging
import json
import pandas as pd # Used fo data framing
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/data_pull") #Need to explicitly add this folder to path
from responses import fetch_data#pylint: disable=import-error

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

#Function to read csv file based on user input..
def get_responses(sheet_name):
    '''Pull the data from the file, produce a dataframe, and parse it into json'''

    #Read the specified file
    file_path = fetch_data(sheet_name)

    #Create a pandas dataframe from the csv file and sheet
    try:
        response_df = pd.read_csv(file_path)
    except (IndexError, FileNotFoundError, NameError, ValueError) as err:
       
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Dataframe for {sheet_name} not created. Message: {err}"
        logging.exception(error)
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: Dataframe for {sheet_name} created."
        logging.info(message)
    
    # Replace NaN values in the dataframe with null
    response_df = response_df.replace(np.nan, 'null')
    
    # Convert datetime fields to string since datetime fields can't be encoded into json
    # If the fields are NaT, convert the value to null
    for col in response_df.select_dtypes([np.datetime64]):
        if np.isnat(response_df[col]):
            response_df[col] = 'null'
        else:
            response_df[col] = response_df[col].astype(str)
    
    #Create a basic list of the dictionaries from the dataframe
    response_dict = response_df.to_dict(orient='records')

    #Create metadata variables to add to each dictionary in the json_list
    metadata_file = f"{sheet_name}.csv"
    metadata_now = datetime.now(tz=timezone.utc) #Need to store the current datetime in UTC time
    metadata_timestamp = metadata_now.strftime('%Y-%m-%d %H:%M:%S')
    metadata_dict = {'metadata_timestamp': metadata_timestamp, 'metadata_file': metadata_file}
    
    #Add the metadata fields to each nested dictionary in the json_list
    for response in response_dict:
        response.update(metadata_dict)

    # Create the json output that will be loaded into postgres
    try:
        responses_json = json.dumps(response_dict, indent=2)
    except ValueError as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Issue converting response data to JSON. Message: {err}"
        logging.exception(error) 
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: Converted response data to JSON."
        logging.info(message)
    
    return responses_json