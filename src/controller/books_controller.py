from src.db.dao.books.dao import BookDAOImpl
from src.models.books_model import Books

# Single instance of BookDAOImpl — Singleton pattern
# Controller never touches the DB directly, always goes through DAO
dao = BookDAOImpl()


def get_all() -> list[Books]:
    return dao.get_all()


def get_by_id(id: int) -> Books:
    return dao.get_by_id(id)


def create_book(book: Books) -> Books:
    return dao.create(book)


def update_book(id: int, book: Books) -> Books:
    return dao.update(id, book)


def delete_book(id: int) -> dict:
    return dao.delete(id)