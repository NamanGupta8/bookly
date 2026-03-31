from src.db.dbo.base_dbo import table_exists, run_query
from fastapi import HTTPException
from src.db.database import db


def create_table() -> None:
    if table_exists("books"):
        print("Books table already exists — skipping creation")
        return
    cursor = db.get_cursor()
    try:
        cursor.execute("""
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publisher VARCHAR(255) NOT NULL,
                published_date VARCHAR(50),
                page_count INT,
                language VARCHAR(50)
            )
        """)
        db.commit()
        print("Books table created successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()