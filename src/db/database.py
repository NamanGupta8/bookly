import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)  # ← add this
class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = psycopg2.connect(DATABASE_URL)
            print("Database connection established")
        return cls._instance
    
    def get_cursor(self):
        return self._connection.cursor()
    
    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()

# Single instance — import this everywhere instead of calling get_connection()
db = Database()
    