'''Use this script to load the track_info and track_metrics tables in the raw 
database'''

# Import libraries
import simplejson as json
import sys
import os
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automaton/core/data_pull")
from track_info import recently_played #pylint: disable=import-error
from track_metrics import features #pylint: disable=import-error
from postgres_connections import pg_conn
from psycopg2 import ProgrammingError

# Establish the necessary variables
db = "raw"
schema = "spotify"
column = "src"
column_type = "json"
info_json = json.dumps(recently_played(), indent=2)
metrics_json = json.dumps(features(), indent=2)
tables = ["track_info", "track_metrics"]

# Open a cursor for the insert statements
conn = pg_conn()
cursor = conn.cursor()

#Top level try block for closing connection and cursor
try:
# Loop through the table list to insert the data into the postgres tables
    try:
        for table in tables:
            if table == "track_info":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS %s.%s.%s (%s %s)''',
                    (db, schema, table, column, column_type)
                    )
                cursor.execute(
                    '''INSERT INTO %s.%s.%s (%s) \nVALUES %s;''', 
                    (db, schema, table, column, info_json)
                    )
                cursor.commit()
            # elif table == "track_metrics":
            #     cursor.execute(f"CREATE TABLE IF NOT EXISTS {schema_table} ({column} {column_type})")
            #     cursor.execute("INSERT INTO " + schema_table + "(" + column + ")" "VALUES(%s);", (metrics))
            #     cursor.commit()
    except ProgrammingError as err:
        print(f"Unable to insert data into postgres. Message: {err}")
finally:
    cursor.close()
    conn.close()