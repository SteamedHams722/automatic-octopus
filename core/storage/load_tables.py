'''Use this script to load the track_info and track_metrics tables in the raw 
database'''

# Import libraries
import simplejson as json
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automaton/core/data_pull")
from tracks import track_features, recently_played #pylint: disable=import-error
from postgres_connections import pg_conn
from psycopg2 import ProgrammingError, sql

# Establish the necessary variables
tables = ["track_info", "track_metrics"]
_, info = recently_played()
features = track_features()

# Open a cursor for the insert statements
conn = pg_conn()
cursor = conn.cursor()

try: #Top level try block for closing connection and cursor
    try:
        # Loop through each table in the list to insert the data. Also creates 
        # the table if it doesn't exist.
       for table in tables:
            cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS spotify.{table} (src jsonb);'''
            )
            #TODO: Find a better way to do this so a hardcoded if is not allowed. ALso,
            # investigate why using the parameterization causes a syntax error
            if table == "track_info":
                cursor.execute('''INSERT INTO spotify.track_info (src) VALUES (%s)''', (info))
            elif table == "track_metrics":
                cursor.execute('''INSERT INTO spotify.track_metrics (src) VALUES (%s)''', (features))
            conn.commit()
    except ProgrammingError as err:
        print(f"Unable to insert data into postgres. Message: {err}")
finally:
    cursor.close()
    conn.close()