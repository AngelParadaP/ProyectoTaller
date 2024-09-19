import os
from dotenv import load_dotenv
import psycopg2

class connection:
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.environ['HOST']
        self.database = os.environ['DATABASE']
        self.user = os.environ['USERNAME']
        self.password = os.environ['PASSWORD']
    
    def open(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        
        return self.conn
    
    def close(self):
        self.conn.close()