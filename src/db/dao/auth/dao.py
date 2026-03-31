from fastapi import HTTPException
from src.db.dao.auth.index import UserDAO
from src.db.dbo import base_dbo as dbo
from src.models.user_model import UserCreate, UserResponse


class UserDAOImpl(UserDAO):

    def create_user(self, user: UserCreate) -> UserResponse:
        # Check if email already exists before inserting
        existing = dbo.fetch_one(
            "SELECT id FROM users WHERE email = %s", (user.email,)
        )
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        row = dbo.run_query_returning("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s) RETURNING *
        """, (user.username, user.email, user.password))
        return self._map(row)

    def get_user_by_email(self, email: str) -> dict:
        # Returns full row including hashed password — needed for login check
        row = dbo.fetch_one(
            "SELECT * FROM users WHERE email = %s", (email,)
        )
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password": row[3],   # hashed password — used for verification
            "created_at": str(row[4])
        }

    def get_user_by_id(self, id: int) -> UserResponse:
        row = dbo.fetch_one(
            "SELECT * FROM users WHERE id = %s", (id,)
        )
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return self._map(row)

    def _map(self, row: tuple) -> UserResponse:
        # Never include password in UserResponse
        return UserResponse(
            id=row[0],
            username=row[1],
            email=row[2],
            created_at=str(row[4])
        )