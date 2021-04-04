"""This will be used to create a user object that can run all of the functions"""
import os
from datetime import datetime
import rollbar
import psycopg2
from postgres_connections import pg_conn  # pylint: disable=import-error

# Create database variables
db = os.getenv("POSTGRES_DB")
schema = "users"


class User:
    """Collects all information needed to pull and load the correct data for each user"""

    def __init__(self, user_id, initials, response_sheet, category):
        """Initialize attributes for Person class"""
        self.user_id = user_id
        self.initials = initials
        self.response_sheet = response_sheet
        self.category = category

    def add_users(self):
        """Add a user object to the dictionary of users"""

        query_users = """
            select
                id as user_id,
                initials,
                response_sheet,
                category
            from {0}.{1}.user_details
            where is_active = 1;'.format(db, schema)"""

        # Open the postgres connection
        with pg_conn() as conn:
            # Open up the SQL cursor so the commands can be executed
            with conn.cursor() as cursor:
                try:
                    execute_query = cursor.execute(query_users)
                    user_results = execute_query.fetchall()
                except (psycopg2.ProgrammingError, psycopg2.errors.SyntaxError) as err:
                    timestamp = datetime.utcnow().replace(microsecond=0)
                    error = f"{timestamp} ERROR: There was an issue creating the {schema} schema. Message: {err}"
                    rollbar.report_message(error)
                except Exception:
                    # Catch-all
                    rollbar.report_exc_info()

        return user_results
