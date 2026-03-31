from src.db.database import db
from fastapi import HTTPException

def table_exists(table_name: str)-> bool:
    cursor = db.get_cursor()
    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = %s
            )
        """, (table_name,))
        return cursor.fetchone()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

def create_table()-> None:
    if table_exists("books"):
        print("Books table already exists- skipping craetion")
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

    def run_query(query: str, params: tuple = ()) -> None:
        cursor = db.get_cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()

    def run_query_returning(query: str, params: tuple = ())-> tuple:
        cursor = db.get_cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            db.commit()
            return row
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    def fetch_one(query: str, params: tuple = ())-> tuple:
        cursor = db.get_cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()

    def fetch_all(query: str, params: tuple = ())-> list:
        cursor = db.get_cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
    
    