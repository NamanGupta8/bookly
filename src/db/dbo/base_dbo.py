from src.db.database import db
from fastapi import HTTPException


# Shared query runner functions — used by both books and auth dbo
# No table-specific logic here, just pure query execution


def run_query(query: str, params: tuple = ()) -> None:
    # For INSERT, UPDATE, DELETE where you dont need the row back
    cursor = db.get_cursor()
    try:
        cursor.execute(query, params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


def run_query_returning(query: str, params: tuple = ()) -> tuple:
    # For INSERT, UPDATE, DELETE with RETURNING — gives back affected row
    cursor = db.get_cursor()
    try:
        cursor.execute(query, params)
        row = cursor.fetchone()
        db.commit()
        return row
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


def fetch_one(query: str, params: tuple = ()) -> tuple:
    # For SELECT — returns single row, None if not found
    cursor = db.get_cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


def fetch_all(query: str, params: tuple = ()) -> list:
    # For SELECT — returns all matching rows
    cursor = db.get_cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


def table_exists(table_name: str) -> bool:
    # Checks if a table exists in the DB — used by all dbo create_table functions
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