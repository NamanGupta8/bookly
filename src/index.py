from fastapi import APIRouter
from src.routes.books import books_api
api = APIRouter()

api.include_router(books_api, prefix="/books", tags=['books'])