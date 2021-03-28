'''Establish a connection to the raw postgres database'''

from datetime import datetime
import psycopg2
import os
import rollbar

def pg_conn ():
    '''Use the environment variables to establish a connection to the postgres
    database where the API data will load. The URL for the Heroku postgres db is
    automatically created in the app config vars'''

    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except (psycopg2.DatabaseError) as err:
        timestamp = datetime.utcnow().replace(microsecond=0)
        error = f"{timestamp} ERROR: There was an issue connecting to postgres. Message: {err}"
        rollbar.report_message(error)
    except Exception:
        #Catch-all
        rollbar.report_exc_info()


    return conn