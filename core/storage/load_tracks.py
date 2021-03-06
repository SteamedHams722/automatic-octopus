# pylint: disable=no-member

"""Use this script to load the track_info and track_metrics tables in the raw 
database"""

# Import libraries
import os
import rollbar
from datetime import datetime
from tracks import track_features, recently_played  # pylint: disable=import-error
from postgres_connections import pg_conn  # pylint: disable=import-error
from psycopg2 import ProgrammingError, errors

# Establish basic Postgeres variables that will be used in both functions
db = os.getenv("POSTGRES_DB")
schema = "spotify"


def tracks_to_pg():
    """This function loads the track features and track info data to their
    respective tables in postgres. If the tables don't exist, it creates them"""

    # Establish the necessary variables
    _, info_json = recently_played()
    info_data = info_json.replace(
        "'", "''"
    )  # Have to escape single quotes in a postgres friendly way
    features_json = track_features()
    features_data = features_json.replace("'", "''")
    table_data = {"track_info": info_data, "track_features": features_data}
    user_id = "e12dfd64bc687b2cb067e8e6116233c3"  # Temporary solution until a more scalable solution is created

    # Open the postgres connection
    with pg_conn() as conn:

        # Open up the SQL cursor so the commands can be executed
        with conn.cursor() as cursor:
            # Create the schema if it doesn't exist
            try:
                create_schema = "create schema if not exists {0};".format(schema)
                cursor.execute(create_schema)
                conn.commit()
            except (
                ProgrammingError,
                errors.InFailedSqlTransaction,
                errors.SyntaxError,
            ) as err:
                timestamp = datetime.utcnow().replace(microsecond=0)
                error = f"{timestamp} ERROR: There was an issue creating the {schema} schema. Message: {err}"
                success = (
                    False  # This will be used to determine what text message to send
                )
                rollbar.report_message(error)
            except Exception:
                # Catch-all
                rollbar.report_exc_info()
            # Loop through each dictionary entry to insert the data. Also creates
            # the table if it doesn't exist.
            for table, data in table_data.items():
                if table == "track_info":
                    create_table = """create table if not exists {0}.{1}.{2} ( 
                    id serial not null primary key,
                    user_id varchar(32),
                    src jsonb not null,
                    created_on_utc timestamp not null
                    );""".format(
                        db, schema, table
                    )
                else:
                    create_table = """create table if not exists {0}.{1}.{2} ( 
                    id serial not null primary key,
                    src jsonb not null,
                    created_on_utc timestamp not null
                    );""".format(
                        db, schema, table
                    )
                try:
                    cursor.execute(create_table)
                    conn.commit()
                except (
                    ProgrammingError,
                    errors.InFailedSqlTransaction,
                    errors.SyntaxError,
                ) as err:
                    timestamp = datetime.utcnow().replace(microsecond=0)
                    error = f"{timestamp} ERROR: There was an issue creating the {table} table. Message: {err}"
                    success = False
                    rollbar.report_message(error)
                except Exception:
                    rollbar.report_exc_info()
                else:
                    timestamp = datetime.utcnow().replace(microsecond=0)
                    if table == "track_info":
                        insert_data = """insert into {0}.{1}.{2} (src, user_id, created_on_utc) 
                        values ('{3}','{4}','{5}');""".format(
                            db, schema, table, data, user_id, timestamp
                        )
                    else:
                        insert_data = """insert into {0}.{1}.{2} (src, created_on_utc) 
                        values ('{3}','{4}');""".format(
                            db, schema, table, data, timestamp
                        )
                    try:
                        cursor.execute(insert_data)
                        conn.commit()
                    except (
                        ProgrammingError,
                        errors.InFailedSqlTransaction,
                        errors.SyntaxError,
                    ) as err:
                        timestamp = datetime.utcnow().replace(microsecond=0)
                        error = f"{timestamp} ERROR:Unable to insert data into the {table} table. Message: {err}"
                        success = False  # This will be used for the text message
                        rollbar.report_message(error)
                    except Exception:
                        rollbar.report_exc_info()
                    else:
                        # Delete duplicate records that are pulled in
                        try:
                            delete_dupes = f"""
                            with unique_only as (
                                select
                                    src::text as src_text,
                                    max(id) as max_id
                                from {schema}.{table}
                                group by 1
                            )
                            delete from {schema}.{table} feat
                            where not exists (
                            select 1 
                            from unique_only unq 
                            where 
                                unq.src_text = feat.src::text 
                                and unq.max_id = feat.id
                            )"""
                            cursor.execute(delete_dupes)
                            conn.commit()
                        except (
                            ProgrammingError,
                            errors.InFailedSqlTransaction,
                            errors.SyntaxError,
                        ) as err:
                            timestamp = datetime.utcnow().replace(microsecond=0)
                            error = f"{timestamp} ERROR:Unable to delete duplicates from the {table} table. Message: {err}"
                            success = False
                            rollbar.report_message(error)
                        except Exception:
                            rollbar.report_exc_info()
                        else:
                            success = True

    return success
