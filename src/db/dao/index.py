from abc import ABC, abstractmethod
from src.models.model import Books


# Abstract class — defines WHAT operations exist, not HOW they work
# Same concept as Java's UserDAO interface from the article
# Any new DAO implementation (e.g. MongoDB) must implement all these methods
class BookDAO(ABC):

    @abstractmethod
    def get_all(self) -> list[Books]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Books:
        pass

    @abstractmethod
    def create(self, book: Books) -> Books:
        pass

    @abstractmethod
    def update(self, id: int, book: Books) -> Books:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass