# Pulls the label data from Google Forms so it can be used as the Y variable in
# the random forest algorithm.

import os
import csv
from datetime import datetime
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')


#Authorization credentials for the Google Sheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
secret_file = os.getenv('service_account')
creds = ServiceAccountCredentials.from_json_keyfile_name(secret_file, scope)
client = gspread.authorize(creds)

#Create a function that pulls the latest responses
def fetch_data(sheet_name): 
    #Create a variable that calls the Google Sheet
    sheet = client.open(sheet_name).sheet1

    #Create a variable that stores the dictionary form of the Google Sheet's results
    form_dict = sheet.get_all_records()

    #Identify each column that will be populated in the CSV file
    csv_columns = sheet.row_values(1) #This returns all the column names from the Google Sheet

    #Create a local CSV file that will hold the data so it can used for data analytics
    #Also, create a local folder to store them if it doesn't exist.
    user_home = os.path.expanduser("~")
    data_dir = os.path.join(user_home, 'automatic-octopus', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    target_csv = data_dir + sheet_name

    #Use a try block in case the write process to the csv file fails
    try:
        with open(target_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in form_dict:
                writer.writerow(data)
    except IOError as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Cannot write to CSV file. Message: {err}"
        logging.exception(error)
    else:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} SUCCESS: Data written to CSV file"
        logging.info(message)
    
    return target_csv