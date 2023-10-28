'''
This configuration script can be executed to create the needed tables in an existing database.
The database information should be specified in /app/database/database.ini
'''

import psycopg2
from app.database.config import config 

def create_tables():
    # table creation commands in the PostgreSQL database
    commands = [
        """
        CREATE TABLE safe (
            owner SERIAL PRIMARY KEY,
            site VARCHAR(255) NOT NULL,
            username VARCHAR(255),
            password VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE users (
            "user" VARCHAR(255) PRIMARY KEY,
            signature VARCHAR(255) NOT NULL
        )
        """]
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()