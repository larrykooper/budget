import os
import psycopg2
from psycopg2 import pool 

from contextlib import contextmanager

host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

dbpool = psycopg2.pool.SimpleConnectionPool(
    2,
    3,
    host=host,
    port=port,
    dbname=db_name,
    user=user,
    password=password,
)

@contextmanager
def db_cursor():
    conn = dbpool.getconn()
    try:
        with conn.cursor() as cur:
            yield cur
            conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        dbpool.putconn(conn)        
    """
    You can have multiple exception types here.
    For example, if you wanted to specifically check for the
    23503 "FOREIGN KEY VIOLATION" error type, you could do:
    except psycopg2.Error as e:
        conn.rollback()
        if e.pgcode = '23503':
            raise KeyError(e.diag.message_primary)
        else
            raise Exception(e.pgcode)
     """
    