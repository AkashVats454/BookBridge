from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    membership_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
