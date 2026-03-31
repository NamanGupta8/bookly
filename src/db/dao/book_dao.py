from fastapi import HTTPException
from src.db.dao.index import BookDAO
from src.db.dbo import book_dbo as dbo
from src.models.model import Books


# Concrete implementation of BookDAO
# Knows WHAT to query — delegates HOW to run it to dbo
class BookDAOImpl(BookDAO):

    def get_all(self) -> list[Books]:
        rows = dbo.fetch_all("SELECT * FROM books")
        return [self._map(row) for row in rows]

    def get_by_id(self, id: int) -> Books:
        row = dbo.fetch_one(
            "SELECT * FROM books WHERE id = %s", (id,)
        )
        if not row:
            raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
        return self._map(row)

    def create(self, book: Books) -> Books:
        row = dbo.run_query_returning("""
            INSERT INTO books (title, author, publisher, published_date, page_count, language)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *
        """, (book.title, book.author, book.publisher, book.published_date, book.page_count, book.language))
        return self._map(row)

    def update(self, id: int, book: Books) -> Books:
        row = dbo.run_query_returning("""
            UPDATE books 
            SET title=%s, author=%s, publisher=%s, published_date=%s, page_count=%s, language=%s
            WHERE id=%s RETURNING *
        """, (book.title, book.author, book.publisher, book.published_date, book.page_count, book.language, id))
        if not row:
            raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
        return self._map(row)

    def delete(self, id: int) -> dict:
        row = dbo.run_query_returning(
            "DELETE FROM books WHERE id = %s RETURNING id", (id,)
        )
        if not row:
            raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
        return {"message": f"Book with id {id} deleted successfully"}

    # Maps a raw DB tuple row to a Books Pydantic model
    # Row order matches the table column order: id, title, author, publisher, published_date, page_count, language
    def _map(self, row: tuple) -> Books:
        return Books(
            id=row[0],
            title=row[1],
            author=row[2],
            publisher=row[3],
            published_date=row[4],
            page_count=row[5],
            language=row[6]
        )