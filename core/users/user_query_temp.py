from postgres_connections import pg_conn  # pylint: disable=import-error

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
        execute_query = cursor.execute(query_users)
        user_results = execute_query.fetchall()
    

print(user_results)
