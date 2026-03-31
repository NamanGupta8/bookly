from fastapi import APIRouter, Depends
from src.models.user_model import UserCreate, UserLogin, UserResponse, TokenResponse
from src.controller.auth_controller import register, login, get_current_user

auth_api = APIRouter()


@auth_api.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate):
    return register(user)


@auth_api.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin):
    return login(user)


# Example of a protected route — requires valid JWT token
# Depends(get_current_user) automatically extracts and verifies the token
# If token is missing or invalid, FastAPI returns 401 automatically
@auth_api.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user