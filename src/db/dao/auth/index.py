from abc import ABC, abstractmethod
from src.models.user_model import UserCreate, UserResponse


class UserDAO(ABC):

    @abstractmethod
    def create_user(self, user: UserCreate) -> UserResponse:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> dict:
        # Returns raw dict including hashed password — needed for login verification
        pass

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserResponse:
        pass