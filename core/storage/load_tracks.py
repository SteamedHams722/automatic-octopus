#pylint: disable=no-member

'''Use this script to load the track_info and track_metrics tables in the raw 
database'''

# Import libraries
import sys
import os
import logging
from datetime import datetime
user_home = os.path.expanduser("~")
sys.path.append(os.path.join(user_home, 'core', 'data_pull'))
from tracks import track_features, recently_played #pylint: disable=import-error
from postgres_connections import pg_conn#pylint: disable=import-error
from psycopg2 import ProgrammingError, errors

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

# Establish basic Postgeres variables that will be used in both functions
db = os.getenv('POSTGRES_DB')
schema = "spotify"

def tracks_to_pg():
    '''This function loads the track features and track info data to their 
    respective tables in postgres. If the tables don't exist, it creates them'''

    # Establish the necessary variables
    _, info_json = recently_played()
    info_data = info_json.replace("'","''") #Have to escape single quotes in a postgres friendly way
    features_json = track_features()
    features_data = features_json.replace("'","''")
    table_data = {'track_info': info_data, 'track_features': features_data}
    user_id = 'e12dfd64bc687b2cb067e8e6116233c3' #Temporary solution until a more scalable solution is created

    # Open the postgres connection
    with pg_conn() as conn:
        timestamp = datetime.utcnow().replace(microsecond=0)
        message = f"{timestamp} Postgres data load initiated."
        logging.info(message)

        # Open up the SQL cursor so the commands can be executed
        with conn.cursor() as cursor:
        #Create the schema if it doesn't exist
            try:
                create_schema = "create schema if not exists {0};".format(schema)
                cursor.execute(create_schema)
                conn.commit()
            except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
                timestamp = datetime.utcnow().replace(microsecond=0)
                error = f"{timestamp} ERROR: There was an issue creating the {schema} schema. Message: {err}"
                success = False #This will be used to determine what text message to send
                logging.exception(error)
            else:
                timestamp = datetime.utcnow().replace(microsecond=0)
                message = f"{timestamp} SUCCESS: The {schema} schema is in the {db} database."
                logging.info(message)

        # Loop through each dictionary entry to insert the data. Also creates 
        # the table if it doesn't exist.
            for table, data in table_data.items():
                if table == 'track_info':
                    create_table = '''create table if not exists {0}.{1}.{2} ( 
                    id serial not null primary key,
                    user_id varchar(32),
                    src json not null,
                    created_on_utc timestamp not null
                    );'''.format(db, schema, table)
                else:
                    create_table = '''create table if not exists {0}.{1}.{2} ( 
                    id serial not null primary key,
                    src json not null,
                    created_on_utc timestamp not null
                    );'''.format(db, schema, table)
                try:
                    cursor.execute(create_table)
                    conn.commit()
                except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
                    timestamp = datetime.utcnow().replace(microsecond=0)
                    error = f"{timestamp} ERROR: There was an issue creating the {table} table. Message: {err}"
                    success = False
                    logging.exception(error)
                else:
                    timestamp = datetime.utcnow().replace(microsecond=0)
                    message = f"{timestamp} SUCCESS: The {table} table is in the {schema} schema."
                    logging.info(message)
                    if table == 'track_info':
                        insert_data = '''insert into {0}.{1}.{2} (src, user_id, created_on_utc) 
                        values ('{3}','{4}','{5}');'''.format(db, schema, table, data, user_id, timestamp)
                    else:
                        insert_data = '''insert into {0}.{1}.{2} (src, created_on_utc) 
                        values ('{3}','{4}');'''.format(db, schema, table, data, timestamp)
                    try:
                        cursor.execute(insert_data)
                        conn.commit()
                    except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
                        timestamp = datetime.utcnow().replace(microsecond=0)
                        error = f"{timestamp} ERROR:Unable to insert data into the {table} table. Message: {err}"
                        success = False  #This will be used for the text message
                        logging.exception(error)
                    else:
                        timestamp = datetime.utcnow().replace(microsecond=0)
                        message = f"{timestamp} SUCCESS: Data was inserted into the {table} table."
                        success = True
                        logging.info(message)

    return success