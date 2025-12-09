from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, engine, Base
from models import Book
from schemas import BookCreate, BookUpdate, BookResponse
import crud


# Create tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Book API",
    description="API for managing books.",
    version="1.0.0",
)


# ========== ROOT ENDPOINT ==========
@app.get("/")
async def root() -> dict:
    """
    Root endpoint providing API information.
    
    Returns:
        dict: Welcome message and available endpoints
    """
    return {
        "message": "Welcome to Book API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "POST /books/ - Add a book (year optional)",
            "GET /books/ - Get all books",
            "GET /books/{id} - Get book by ID",
            "PUT /books/{id} - Update book",
            "DELETE /books/{id} - Delete book",
            "GET /books/search/ - Search books"
        ]
    }


# ========== POST /books/ ==========
@app.post("/books/", 
          response_model=BookResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Add a new book",
          tags=["Books"])
async def add_book(book: BookCreate, db: Session = Depends(get_db)) -> BookResponse:
    """
    Add a new book to the database.
    
    Args:
        book (BookCreate): Book data for creation
        db (Session): Database session
        
    Returns:
        BookResponse: Created book
        
    Notes:
        Year field is optional.
        Example without year:
        ```json
        {
            "title": "Book Title",
            "author": "Author Name"
        }
        ```
    """
    return crud.create_book(db, book)


# ========== GET /books/ ==========
@app.get("/books/",
         response_model=List[BookResponse],
         summary="Get all books",
         tags=["Books"])
async def get_all_books_endpoint(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
) -> List[BookResponse]:
    """
    Retrieve all books from the database.
    
    Args:
        skip (int): Number of records to skip (default 0)
        limit (int): Number of records to return (default 100, max 1000)
        db (Session): Database session
        
    Returns:
        List[BookResponse]: List of all books
    """
    return crud.get_all_books(db, skip=skip, limit=limit)


# ========== GET /books/search/ ==========
@app.get("/books/search/",
         response_model=List[BookResponse],
         summary="Search books",
         tags=["Search"])
async def search_books_endpoint(
    title: Optional[str] = Query(None, description="Search by title (partial match)"),
    author: Optional[str] = Query(None, description="Search by author (partial match)"),
    year: Optional[int] = Query(None, description="Search by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
) -> List[BookResponse]:
    """
    Search books by title, author, or year.
    
    Args:
        title (Optional[str]): Title to search for
        author (Optional[str]): Author to search for
        year (Optional[int]): Publication year to search for
        skip (int): Number of records to skip
        limit (int): Number of records to return
        db (Session): Database session
        
    Returns:
        List[BookResponse]: List of matching books
        
    Examples:
        - `/books/search/?author=Tolstoy` - Books by Tolstoy
        - `/books/search/?title=war&author=tolstoy` - Books with "war" in title by Tolstoy
        - `/books/search/?year=1869` - Books from 1869
        
    Note:
        Searching by year will only return books with the specified year.
        Books without a year will not be included in year search results.
    """
    return crud.search_books(db, title=title, author=author, year=year, skip=skip, limit=limit)


# ========== PUT /books/{book_id} ==========
@app.put("/books/{book_id}",
         response_model=BookResponse,
         summary="Update book information",
         tags=["Books"])
async def update_book_endpoint(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
) -> BookResponse:
    """
    Update book information.
    
    Args:
        book_id (int): ID of the book to update
        book_update (BookUpdate): Updated book data
        db (Session): Database session
        
    Returns:
        BookResponse: Updated book
        
    Raises:
        HTTPException: 404 if book not found
        
    Notes:
        Can update one, several, or all fields.
        To remove year, pass `"year": null`.
        
        Example for removing year:
        ```json
        {
            "year": null
        }
        ```
    """
    db_book = crud.update_book(db, book_id, book_update)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return db_book


# ========== DELETE /books/{book_id} ==========
@app.delete("/books/{book_id}",
            summary="Delete a book",
            tags=["Books"])
async def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a book by ID.
    
    Args:
        book_id (int): ID of the book to delete
        db (Session): Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if book not found
    """
    success: bool = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return {"message": f"Book with ID {book_id} successfully deleted"}


# Start server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)