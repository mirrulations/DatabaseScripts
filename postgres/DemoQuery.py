import os
import psycopg
from dotenv import load_dotenv

def run_query():
   
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
    }

    # Query to retrieve fields with comment that has specified comment_id
    query = """
    SELECT 
        d.docket_id AS Docket_ID, 
        d.docket_title AS Docket_Title, 
        c.comment AS Comment
    FROM dockets AS d
    JOIN comments AS c ON c.docket_id = d.docket_id
    WHERE c.comment_id = %s;
    """

    comment_id = "DOS-2022-0004-0003" # Set to desired comment_id

    try:
        with psycopg.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (comment_id,))
                results = cursor.fetchall()

                # Display results
                for row in results:
                    docket_id, docket_title, comment = row  # Unpacking tuple
                    print(f"Docket_ID: {docket_id}\nDocket_Title: {docket_title}\nComment: {comment}")

    except psycopg.Error as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    run_query()
