
import psycopg2
from config import config

def insert_vendor_list(manca_testing,vendor_id, vendor_name):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO manca_testing(vendor_id, vendor_name) VALUES(vendor_id,vendor_name)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,manca_testing)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
