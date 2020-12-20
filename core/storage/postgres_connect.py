'''Establish a connection to the raw postgres database'''

from psycopg2 import connect
from os import getenv

db = getenv("postgres_db")
user = getenv("postgres_user")
pwd = getenv("postgres_pwd")
host = getenv("postgres_host")
port = getenv("postgres_port")

conn = connect(dbname = db, user = user, password = pwd, host = host, port = port)