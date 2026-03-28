from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel
from src.index import api
app = FastAPI()

class BookCreateModel(BaseModel):
    title: str
    author: str


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Server working"}

# Any parameter in function, will be considered a query parameter if not defined in path. Defined in path is path parameter
@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0)-> dict[str, str]:
    return {"message": f"Hello {name} !! Age {age}"}

@app.post('/create_book')
async def create_book(book_data: BookCreateModel)-> dict[str, str]:
    return {
        "title": book_data.title,
        "author": book_data.author
        }

@app.get('/get_headers')
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    return request_headers

app.include_router(api)