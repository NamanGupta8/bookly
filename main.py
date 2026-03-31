from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel
from src.index import api
from src.db.database import db
from src.db.dbo.book_dbo import create_table

app = FastAPI(title="Bookly", version="1.0.0")

create_table()

class BookCreateModel(BaseModel):
    title: str
    author: str


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Server working"}



app.include_router(api)