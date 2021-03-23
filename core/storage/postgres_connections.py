'''Establish a connection to the raw postgres database'''

from psycopg2 import connect
import os
database = os.getenv("postgres_db")
user = os.getenv("postgres_user")
password = os.getenv("postgres_pwd")
host = os.getenv("postgres_host")
port = os.getenv("postgres_port")

def pg_conn ():
    '''Use the environment variables to establish a connection to the postgres
    database where the API data will load'''
    conn = connect(
        dbname = database,
        user = user, 
        password = password,
        host = host,
        port = port
    )
    
    return conn