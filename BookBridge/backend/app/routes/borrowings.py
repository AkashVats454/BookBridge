from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.models.borrowing import Borrowing
from app.models.book import Book
from app.models.member import Member
from app.schemas.borrowing import (
    BorrowingCreate,
    BorrowingResponse,
    BorrowingReturnResponse,
)
from typing import List

router = APIRouter(prefix="/borrowings", tags=["borrowings"])


@router.post("/", response_model=BorrowingResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(borrowing: BorrowingCreate, db: Session = Depends(get_db)):
    """Record a book borrowing."""
    # Verify book exists
    db_book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # Verify member exists
    db_member = db.query(Member).filter(Member.id == borrowing.member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    # Check if book is available
    if db_book.available_copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No copies available for this book",
        )

    # Check if member already has this book checked out
    existing_borrow = (
        db.query(Borrowing)
        .filter(
            Borrowing.book_id == borrowing.book_id,
            Borrowing.member_id == borrowing.member_id,
            Borrowing.is_returned == False,
        )
        .first()
    )
    if existing_borrow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already has this book checked out",
        )

    # Create borrowing record
    db_borrowing = Borrowing(**borrowing.dict())
    db_book.available_copies -= 1

    db.add(db_borrowing)
    db.add(db_book)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


@router.get("/", response_model=List[BorrowingResponse])
def list_borrowings(
    skip: int = 0,
    limit: int = 10,
    is_returned: bool = None,
    db: Session = Depends(get_db),
):
    """Get list of all borrowings."""
    query = db.query(Borrowing)

    if is_returned is not None:
        query = query.filter(Borrowing.is_returned == is_returned)

    borrowings = query.offset(skip).limit(limit).all()
    return borrowings


@router.get("/member/{member_id}", response_model=List[BorrowingResponse])
def get_member_borrowings(
    member_id: int, is_returned: bool = False, db: Session = Depends(get_db)
):
    """Get all borrowings for a specific member."""
    # Verify member exists
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    borrowings = (
        db.query(Borrowing)
        .filter(Borrowing.member_id == member_id, Borrowing.is_returned == is_returned)
        .all()
    )
    return borrowings


@router.get("/{borrowing_id}", response_model=BorrowingResponse)
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    """Get a specific borrowing record by ID."""
    db_borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()
    if not db_borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing record not found"
        )
    return db_borrowing


@router.post("/{borrowing_id}/return", response_model=BorrowingReturnResponse)
def return_book(borrowing_id: int, db: Session = Depends(get_db)):
    """Record a book return."""
    db_borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()
    if not db_borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing record not found"
        )

    if db_borrowing.is_returned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book has already been returned",
        )

    # Update borrowing record
    db_borrowing.is_returned = True
    db_borrowing.returned_date = datetime.utcnow()

    # Update book availability
    db_book = db.query(Book).filter(Book.id == db_borrowing.book_id).first()
    db_book.available_copies += 1

    db.add(db_borrowing)
    db.add(db_book)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


@router.get("/overdue/list", response_model=List[BorrowingResponse])
def get_overdue_borrowings(db: Session = Depends(get_db)):
    """Get all overdue borrowings."""
    borrowings = (
        db.query(Borrowing)
        .filter(Borrowing.is_returned == False)
        .all()
    )
    overdue = [b for b in borrowings if b.is_overdue]
    return overdue
