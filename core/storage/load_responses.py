# pylint: disable=no-member

#Import libraries
import sys
import os
import logging
from datetime import datetime
user_home = os.path.expanduser("~").replace(os.sep,'/')
sys.path.append(user_home + r"/automatic-octopus/core/data_prep")
from responses_prep import get_responses#pylint: disable=import-error
from postgres_connections import pg_conn
from psycopg2 import ProgrammingError, errors

# Set-up logging
logging.basicConfig(filename='execute.log', filemode='a', level='INFO')

def responses_to_pg(sheet_name):
  '''This function loads the json responses data into postgres'''

# Establish the necessary variables
  db = "nucleus"
  schema = "surveys"
  responses_json = get_responses(sheet_name)
  responses_data = responses_json.replace("'","''") #Have to escape single quotes in a postgres friendly way
  table = "responses"
  # Open a cursor for the insert statements
  conn = pg_conn()
  cursor = conn.cursor()

  try: #Top level try block for closing connection and cursor
      timestamp = datetime.utcnow().replace(microsecond=0)
      message = f"{timestamp} Postgres data load initiated."
      logging.info(message)

      # Open up the SQL cursor so the commands can be executed
      with cursor:
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

          # Create the table if it doesn't exist
          try:
              create_table = '''create table if not exists {0}.{1}.{2} ( 
                  id serial not null primary key,
                  src json not null,
                  created_on_utc timestamp not null
                  );'''.format(db, schema, table)
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

          # Load the response data into postgres. The json_array_elements can be
          # used to expand them out further.
          try:
              timestamp = datetime.utcnow().replace(microsecond=0)
              insert_data = '''insert into {0}.{1}.{2} (src, created_on_utc) 
                  values ('{3}','{4}');'''.format(db, schema, table, responses_data, timestamp)
              cursor.execute(insert_data)
              conn.commit()

              #Delete the old data since it's not necessary anymore. Doing this separately
              # from the table create because if the data fails to load I don't want to lose
              # the previous data
              delete_old = "delete from {0}.{1}.{2} where created_on_utc < '{3}'".format(db, schema, table, timestamp)
              cursor.execute(delete_old)
              conn.commit()
          except (ProgrammingError, errors.InFailedSqlTransaction, errors.SyntaxError) as err:
              timestamp = datetime.utcnow().replace(microsecond=0)
              error = f"{timestamp} ERROR:Unable to insert data into the {table} table. Message: {err}"
              success = False #This will be used for the text message
              logging.exception(error)
          else:
              timestamp = datetime.utcnow().replace(microsecond=0)
              message = f"{timestamp} SUCCESS: Data was inserted into the {table} table."
              success = True
              logging.info(message)
  finally:
      conn.close()
      timestamp = datetime.utcnow().replace(microsecond=0)
      message = f"{timestamp} Connection closed."
      logging.info(message)
      
  return success


#Use for testing
# responses_to_pg(os.environ['response_sheet'])