from fastapi import APIRouter
from src.db.MOCK_DATA import data 
from src.models.model import Books 
from src.controller.controller import get_all, get_by_id
books_api = APIRouter()

@books_api.get('/')
async def get_all_books()-> list[Books]:
    return get_all(data)

@books_api.get('/{book_id}')
async def get_book(book_id: int) -> Books:
    return get_by_id(data, book_id)

@books_api.post('/')
async def create_book() -> Books:
    pass

@books_api.put('/{book_id}')
async def update_book(book_id: int)-> Books:
    pass

@books_api.delete('/{book_id}')
async def delete_book(book_id: int)-> dict:
    pass