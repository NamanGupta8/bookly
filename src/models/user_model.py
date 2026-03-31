from pydantic import BaseModel, EmailStr
from typing import Optional


# Used when REGISTERING — what the user sends
class UserCreate(BaseModel):
    username: str
    email: EmailStr      # EmailStr validates email format automatically
    password: str


# Used when LOGGING IN
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Used in RESPONSES — never expose password
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[str] = None


# Returned after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # standard JWT token type