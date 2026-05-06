from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    description: Optional[str] = None
    total_copies: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: Optional[str] = None
    total_copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
