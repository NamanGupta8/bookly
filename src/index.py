from fastapi import APIRouter
from src.routes.books import books_api
from src.routes.auth import auth_api

api = APIRouter()

# Add new routers here — main.py never needs to change
api.include_router(books_api, prefix="/books", tags=["Books"])
api.include_router(auth_api, prefix="/auth", tags=["Auth"])