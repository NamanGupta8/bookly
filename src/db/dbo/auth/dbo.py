from src.db.dbo.base_dbo import table_exists
from fastapi import HTTPException
from src.db.database import db


def create_table() -> None:
    if table_exists("users"):
        print("Users table already exists — skipping creation")
        return
    cursor = db.get_cursor()
    try:
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        db.commit()
        print("Users table created successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()