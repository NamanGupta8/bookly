from fastapi import HTTPException

from src.models.model import Books

def get_all(books: list[Books]):
    return books

def get_by_id(books: list[Books], id: int):
    return list(filter(lambda book: book['id']== id, books))

def create_book(books: list[Books], book: Books) -> Books:
    books.append(book)
    return book

def update_book(id: int, book:Books):
    for data in book:
        if(data['id'] == id):
            data = book
            return book
    return None 

def delete_book(books: list[Books], id: int) -> dict:
    filtered = list(filter(lambda b: b['id'] == id, books))
    if not filtered:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    books.remove(filtered[0])
    return {"message": f"Book with id {id} deleted successfully"}