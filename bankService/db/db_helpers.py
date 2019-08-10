import psycopg2
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


def connectToDB():
  try:
    # Connect to an existing database
    conn = psycopg2.connect("dbname={} user={}".format(
        os.environ.get('DB_NAME'), os.environ.get('DB_USER')))

    # Open a cursor to perform database operations
    cur = conn.cursor()

    return conn, cur
  except Exception as e:
    print("Some error occurred while connecting to the database")
