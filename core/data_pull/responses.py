# Pulls the label data from Google Forms so it can be used as the Y variable in
# the random forest algorithm.

import os
import csv
from datetime import datetime
import rollbar
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authorization credentials for the Google Sheet
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
secret_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
creds = ServiceAccountCredentials.from_json_keyfile_name(secret_file, scope)
client = gspread.authorize(creds)


def fetch_data(sheet_name):
    """Pull data from the Google Sheet that stores the label response data"""

    # Create a variable that calls the Google Sheet
    sheet = client.open(sheet_name).sheet1
    # Create a variable that stores the dictionary form of the Google Sheet's results
    form_dict = sheet.get_all_records()
    # Identify each column that will be populated in the CSV file
    csv_columns = sheet.row_values(
        1
    )  # This returns all the column names from the Google Sheet
    # Create a local CSV file that will hold the data so it can used for data analytics
    # Also, create a local folder to store them if it doesn't exist.
    data_dir = os.path.join(os.path.expanduser("~"), "automatic-octopus", "data")
    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        target_csv = data_dir + sheet_name
    except OSError as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f" {timestamp} ERROR: There was an issue creating the directory. Message: {err}"
        rollbar.report_message(error)
    except Exception:
        # Catch-all
        rollbar.report_exc_info()
    # Use a try block in case the write process to the csv file fails
    try:
        with open(target_csv, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in form_dict:
                writer.writerow(data)
    except IOError as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: Cannot write to CSV file. Message: {err}"
        rollbar.report_message(error)
    except Exception:
        rollbar.report_exc_info()

    return target_csv
