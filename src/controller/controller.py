from src.models.model import Books

def get_all(books: list[Books]):
    return books

def get_by_id(books: list[Books], id: int):
    return list(filter(lambda book: book['id']== id, books))

def create_book(book:Book):
    pass

def update_book():
    pass

def delete_book():
    pass