from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.database import Base


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    borrowed_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14), nullable=False)
    returned_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    book = relationship("Book", back_populates="borrowings")
    member = relationship("Member", back_populates="borrowings")

    @property
    def is_overdue(self):
        if not self.is_returned and datetime.utcnow() > self.due_date:
            return True
        return False

    def __repr__(self):
        return f"<Borrowing(id={self.id}, book_id={self.book_id}, member_id={self.member_id})>"
