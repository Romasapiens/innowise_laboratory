from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Book
from schemas import BookCreate, BookUpdate
from typing import List, Optional


def create_book(db: Session, book: BookCreate) -> Book:
    """
    Create a new book in the database.
    
    Args:
        db (Session): Database session
        book (BookCreate): Book data for creation
        
    Returns:
        Book: Created book object
    """
    db_book: Book = Book(
        title=book.title,
        author=book.author,
        year=book.year  # Can be None
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """
    Get a book by its ID.
    
    Args:
        db (Session): Database session
        book_id (int): ID of the book to retrieve
        
    Returns:
        Optional[Book]: Book object if found, None otherwise
    """
    return db.query(Book).filter(Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """
    Get all books with pagination.
    
    Args:
        db (Session): Database session
        skip (int): Number of records to skip (default 0)
        limit (int): Maximum number of records to return (default 100)
        
    Returns:
        List[Book]: List of book objects
    """
    return db.query(Book).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    """
    Update a book's information.
    
    Args:
        db (Session): Database session
        book_id (int): ID of the book to update
        book_update (BookUpdate): Updated book data
        
    Returns:
        Optional[Book]: Updated book object if found, None otherwise
    """
    db_book: Optional[Book] = get_book(db, book_id)
    if not db_book:
        return None
    
    update_data: dict = book_update.model_dump(exclude_unset=True)
    
    # If year is explicitly passed as null (None), remove the year
    if 'year' in update_data and update_data['year'] is None:
        db_book.year = None
        del update_data['year']
    
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """
    Delete a book by ID.
    
    Args:
        db (Session): Database session
        book_id (int): ID of the book to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    db_book: Optional[Book] = get_book(db, book_id)
    if not db_book:
        return False
    
    db.delete(db_book)
    db.commit()
    return True


def search_books(
    db: Session, 
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Book]:
    """
    Search books by various criteria.
    
    Args:
        db (Session): Database session
        title (Optional[str]): Title to search for (partial match)
        author (Optional[str]): Author to search for (partial match)
        year (Optional[int]): Publication year to search for
        skip (int): Number of records to skip (default 0)
        limit (int): Maximum number of records to return (default 100)
        
    Returns:
        List[Book]: List of book objects matching the criteria
    """
    query = db.query(Book)
    
    # Add search conditions if parameters are provided
    filters: list = []
    if title:
        filters.append(Book.title.ilike(f"%{title}%"))
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))
    if year:
        filters.append(Book.year == year)
    
    # Apply filters (logical AND)
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()