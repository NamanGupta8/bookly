from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.db.dao.auth.dao import UserDAOImpl
from src.models.user_model import UserCreate, UserLogin, UserResponse, TokenResponse
import os

# -----------------------------------------------
# Password hashing setup
# bcrypt is the industry standard for hashing passwords
# -----------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------------------------
# JWT setup
# -----------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"                 # hashing algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # token expires after 30 minutes

# OAuth2PasswordBearer tells FastAPI where to find the token in the request
# tokenUrl is the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

dao = UserDAOImpl()


def hash_password(password: str) -> str:
    # Converts plain text password to bcrypt hash
    # e.g. "mypassword123" → "$2b$12$..." (irreversible)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Checks if plain password matches the stored hash
    # bcrypt handles this internally — you never decrypt, you re-hash and compare
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    # Creates a JWT token with an expiry time
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # add expiry to payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def register(user: UserCreate) -> UserResponse:
    # Hash the password before storing — never save plain text
    user.password = hash_password(user.password)
    return dao.create_user(user)


def login(user: UserLogin) -> TokenResponse:
    # Fetch user by email — includes hashed password
    db_user = dao.get_user_by_email(user.email)

    # Verify the password the user sent against the stored hash
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Create JWT token with user's email as the subject
    token = create_access_token({"sub": db_user["email"], "id": db_user["id"]})
    return TokenResponse(access_token=token)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    # This is a FastAPI dependency — inject into any protected route
    # It reads the token from the Authorization header, verifies it, returns the user
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return dao.get_user_by_email(email)