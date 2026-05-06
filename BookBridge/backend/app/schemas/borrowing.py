from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BorrowingCreate(BaseModel):
    book_id: int
    member_id: int


class BorrowingResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime] = None
    is_returned: bool
    is_overdue: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BorrowingReturnResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: datetime
    is_returned: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
