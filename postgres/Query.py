import os
import sys
import psycopg
import sqlparse
import json
from psycopg.rows import dict_row
from dotenv import load_dotenv


def is_safe_query(query):
    """
    Validate if the query is a safe SELECT statement.
    Disallows actions like INSERT, UPDATE, DELETE, DROP, etc.
    """
    parsed_query = sqlparse.parse(query)

    for statement in parsed_query:
        if statement.get_type() != "SELECT":
            return False
    return True

def run_query(user_query=None, params=None):
    '''
    Execute a user-provided query against the PostgreSQL database.
    '''

    load_dotenv()

    dbname = os.getenv("POSTGRES_DB")
    username = os.getenv("POSTGRES_USERNAME")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn_params = {
        "dbname": dbname,
        "user": username,
        "password": password,
        "host": host,
        "port": port,
        "row_factory": dict_row  # Fetch results as dictionaries
    }

    # Use user query if provided; otherwise, prompt for a query
    user_query =  user_query or input("No query provided. Please provide a query to execute.\n").strip()

    # Check if the query is provided and is safe
    if not user_query:
        print("No query provided, exiting.")
        return
    if not is_safe_query(user_query):
        print("Unsafe query detected! Only SELECT statements are allowed.")
        return

    try:
        with psycopg.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(user_query, params if params else ())
                results = cursor.fetchall()

                # Display results in JSON format
                if results:
                    print(json.dumps(results, indent=4, default=str))
                else:
                    print("Query executed successfully, but no records were found.")
    except psycopg.Error as e:
        print(f"Query failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])  # Join all args as a query
    else:
        user_query = None  # No user query provided, use default

    run_query(user_query)
