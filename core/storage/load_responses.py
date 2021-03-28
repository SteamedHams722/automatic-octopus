# pylint: disable=no-member

#Import libraries
import sys
import os
import rollbar
from datetime import datetime
user_home = os.path.expanduser("~")
sys.path.append(os.path.join(user_home, 'core', 'data_prep'))
from responses_prep import get_responses#pylint: disable=import-error
from postgres_connections import pg_conn#pylint: disable=import-error
from psycopg2 import ProgrammingError, errors

def responses_to_pg(sheet_name):
    '''This function loads the json responses data into postgres'''

    # Establish the necessary variables
    db = os.getenv('POSTGRES_DB')
    schema = 'survey'
    responses_json = get_responses(sheet_name)
    responses_data = responses_json.replace("'","''") #Have to escape single quotes in a postgres friendly way
    user_id = 'e12dfd64bc687b2cb067e8e6116233c3' #Temporary solution until a more scalable solution is created
    table = "responses"

    # Open the connection to the postgres db
    with pg_conn() as conn:
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
                rollbar.report_message(error)
            except Exception:
                rollbar.report_exc_info()
            # Create the table if it doesn't exist
            try:
                create_table = '''create table if not exists {0}.{1}.{2} ( 
                id serial not null primary key,
                user_id varchar(32) not null,
                src json not null,
                created_on_utc timestamp not null
                );'''.format(db, schema, table)
                cursor.execute(create_table)
                conn.commit()
            except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
                timestamp = datetime.utcnow().replace(microsecond=0)
                error = f"{timestamp} ERROR: There was an issue creating the {table} table. Message: {err}"
                success = False
                rollbar.report_message(error)
            except Exception:
                rollbar.report_exc_info()
          # Load the response data into postgres. The json_array_elements can be
          # used to expand them out further.
            try:
                timestamp = datetime.utcnow().replace(microsecond=0)
                insert_data = '''insert into {0}.{1}.{2} (user_id, src, created_on_utc) 
                values ('{3}','{4}', '{5}');'''.format(db, schema, table, user_id, responses_data, timestamp)
                cursor.execute(insert_data)
                conn.commit()
            except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
                timestamp = datetime.utcnow().replace(microsecond=0)
                error = f"{timestamp} ERROR:Unable to insert data into the {table} table. Message: {err}"
                success = False #This will be used for the text message
                rollbar.report_message(error)
            except Exception:
                rollbar.report_exc_info()
            else:
                #Delete the old data since it's not necessary anymore. Doing this separately
                # from the table create because if the data fails to load I don't want to lose
                # the previous data
                delete_old = "delete from {0}.{1}.{2} where created_on_utc < '{3}'".format(db, schema, table, timestamp)
                cursor.execute(delete_old)
                conn.commit()
                success = True

    return success