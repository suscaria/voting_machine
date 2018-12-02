
import psycopg2
from config import config


class ConnectDB:
    def __init__(self):
        self.cur = self.create_conn()

    def create_conn(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the db...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        return cur

    def insert(self, query):
        self.cur.execute(query)


if __name__ == '__main__':
    con = ConnectDB()
    #con.insert("insert into manca.round1 values(%d,%d,%s,%s,%d,%s)" % (current_batch_id, sequence_id, receiver, contestant_name, contestant_mark, local_date)")
