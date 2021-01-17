#pylint: disable=no-member
'''Use this script to load the track_info and track_metrics tables in the raw 
database'''

# Import libraries
import sys
import os
import logging
from datetime import datetime
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automaton/core/data_pull")
#from tracks import track_features, recently_played#pylint: disable=import-error
from postgres_connections import pg_conn
from psycopg2 import ProgrammingError, errors

# Establish the necessary variables
db = "raw"
schema = "spotify"
info_data = 'Homer' #Temp until I can get the spotify data working
feature_data = 'Burnsie' #Temp until I can get the spotify data working
table_data = {"track_info": info_data, "track_metrics": feature_data}

# Set-up logging
logging.basicConfig(filename='load.log', filemode='a', level=logging.DEBUG)

# Open a cursor for the insert statements
conn = pg_conn()
cursor = conn.cursor()

try: #Top level try block for closing connection and cursor
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f"{timestamp} Postgres data load initiated."
    logging.exception(message)

    # Open up the SQL cursor so the commands can be executed
    with cursor:

        #Create the schema if it doesn't exist
        try:
            create_schema = "create schema if not exists {0};".format(schema)
            cursor.execute(create_schema)
            conn.commit()
        except (ProgrammingError, errors.InFailedSqlTransaction) as err:
            timestamp = datetime.utcnow().replace(microsecond=0)
            error = f"{timestamp} ERROR: There was an issue creating the {schema} schema. Message: {err}"
            logging.exception(message)
        else:
            timestamp = datetime.utcnow().replace(microsecond=0)
            message = f"{timestamp} SUCCESS: The {schema} schema is in the {db} database."
            logging.exception(message)

            # Loop through each dictionary entry to insert the data. Also creates 
            # the table if it doesn't exist.
        for table, data in table_data.items():
            try:
                create_table = "create table if not exists {0}.{1}.{2} (src varchar(50));".format(db, schema, table)
                cursor.execute(create_table)
                conn.commit()
            except (ProgrammingError, errors.InFailedSqlTransaction) as err:
                timestamp = datetime.utcnow().replace(microsecond=0)
                error = f"{timestamp} ERROR: There was an issue creating the {table} table. Message: {err}"
                logging.exception(message)
            else:
                timestamp = datetime.utcnow().replace(microsecond=0)
                message = f"{timestamp} SUCCESS: The {table} table is in the {schema} schema."
                logging.exception(message)
            
            try:
                insert_data = "insert into {0}.{1}.{2} values ('{3}');".format(db, schema, table, data)
                cursor.execute(insert_data)
                conn.commit()
            except (ProgrammingError, errors.InFailedSqlTransaction) as err:
                message = f"Unable to insert data into the {table} table. Message: {err}"
                logging.exception(message)
            else:
                timestamp = datetime.utcnow().replace(microsecond=0)
                message = f"{timestamp} SUCCESS: Data was inserted into the {table} table."
                logging.exception(message)
finally:
    conn.close()
    timestamp = datetime.utcnow().replace(microsecond=0)
    message = f"{timestamp} Postgres data load completed. Connection closed."
    logging.exception(message)
