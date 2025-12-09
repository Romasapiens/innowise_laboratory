from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    """
    Pydantic schema for creating a book.
    
    Attributes:
        title (str): Book title (required)
        author (str): Book author (required)
        year (Optional[int]): Publication year (optional)
    """
    
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")
    year: Optional[int] = Field(None, ge=1000, le=2100, description="Publication year (optional)")
    
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate year is not in the future.
        
        Args:
            v (Optional[int]): Year value
            
        Returns:
            Optional[int]: Validated year
            
        Raises:
            ValueError: If year is in the future
        """
        if v is not None:
            current_year: int = datetime.now().year
            if v > current_year:
                raise ValueError(f'Year cannot be in the future. Current year: {current_year}')
        return v
    
    class Config:
        json_schema_extra: dict = {
            "example": {
                "title": "War and Peace",
                "author": "Leo Tolstoy",
                "year": 1869
            },
            "example2": {
                "title": "New Book",
                "author": "Author",
                "year": None  # Without year
            }
        }


class BookUpdate(BaseModel):
    """
    Pydantic schema for updating a book.
    
    Attributes:
        title (Optional[str]): Book title
        author (Optional[str]): Book author
        year (Optional[int]): Publication year
    """
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate year is not in the future.
        
        Args:
            v (Optional[int]): Year value
            
        Returns:
            Optional[int]: Validated year
            
        Raises:
            ValueError: If year is in the future
        """
        if v is not None:
            current_year: int = datetime.now().year
            if v > current_year:
                raise ValueError(f'Year cannot be in the future. Current year: {current_year}')
        return v
    
    class Config:
        json_schema_extra: dict = {
            "example": {
                "title": "War and Peace",
                "author": "Lev Nikolayevich Tolstoy",
                "year": 1867
            }
        }


class BookResponse(BaseModel):
    """
    Pydantic schema for book responses.
    
    Attributes:
        id (int): Book ID
        title (str): Book title
        author (str): Book author
        year (Optional[int]): Publication year
    """
    
    id: int
    title: str
    author: str
    year: Optional[int] = None
    
    class Config:
        from_attributes: bool = True  # Enables ORM mode for SQLAlchemy models