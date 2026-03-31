from fastapi import APIRouter
from src.models.books_model import Books
from src.controller.controller import get_all, get_by_id, create_book, update_book, delete_book

books_api = APIRouter()


@books_api.get('/')
async def get_all_books() -> list[Books]:
    return get_all()


@books_api.get('/{book_id}')
async def get_book(book_id: int) -> Books:
    return get_by_id(book_id)


@books_api.post('/', status_code=201)
async def add_book(book: Books) -> Books:
    return create_book(book)


@books_api.put('/{book_id}')
async def modify_book(book_id: int, book: Books) -> Books:
    return update_book(book_id, book)


@books_api.delete('/{book_id}')
async def remove_book(book_id: int) -> dict:
    return delete_book(book_id)