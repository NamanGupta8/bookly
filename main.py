from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel
from src.index import api
from src.db.database import db
from src.db.dbo.books.dbo import create_table as create_books_table
from src.db.dbo.auth.dbo import create_table as create_auth_table
app = FastAPI(title="Bookly", version="1.0.0")

create_books_table()
create_auth_table()

class BookCreateModel(BaseModel):
    title: str
    author: str


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Server working"}



app.include_router(api)