'''Establish a connection to the raw postgres database'''

from psycopg2 import connect
from os import getenv

db = getenv("postgres_db")
user = getenv("postgres_user")
pwd = getenv("postgres_pwd")
host = getenv("postgres_host")
port = getenv("postgres_port")

def pg_conn ():
    '''Use the environment variables to establish a connection to the postgres
    database where the API data will load'''
    conn = connect(
        dbname = db,
        user = user, 
        password = pwd,
        host = host,
        port = port
    )
    return conn
