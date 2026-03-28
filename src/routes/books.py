from fastapi import APIRouter
from src.db.MOCK_DATA import data, next_id 
from src.models.model import Books 
from src.controller.controller import get_all, get_by_id, create_book, update_book as update, delete_book as delete
books_api = APIRouter()

@books_api.get('/')
def get_all_books()-> list[Books]:
    return get_all(data)

@books_api.get('/{book_id}')
def get_book(book_id: int) -> Books:
    return get_by_id(data, book_id)

@books_api.post('/')
def add_book(book: Books) -> Books:
    # Assign the next available id
    global next_id 
    book.id = next_id
    next_id += 1
    return create_book(data, book)

@books_api.put('/{book_id}')
def update_book(book_id: int)-> Books:
    return update(book_id, data)

@books_api.delete('/{book_id}')
def delete_book(book_id: int)-> dict:
    return delete(data, book_id)