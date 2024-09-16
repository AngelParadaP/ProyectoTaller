import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

class connection:
    def __init__(self) -> None:
        self.host = os.environ.get("HOST")
        self.database = os.environ.get("DATABASE")
        self.user = os.environ.get("USER")
        self.password = os.environ.get("PASSWORD")
    
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