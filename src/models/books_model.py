from typing import Optional
from pydantic import BaseModel

class Books(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str