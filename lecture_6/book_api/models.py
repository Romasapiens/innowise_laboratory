from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    """
    SQLAlchemy model representing a book in the database.
    
    Attributes:
        id (int): Primary key, auto-incremented
        title (str): Book title, indexed and required
        author (str): Book author, indexed and required
        year (int, optional): Publication year, nullable
    """
    
    __tablename__: str = "books"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    title: Column = Column(String, index=True, nullable=False)
    author: Column = Column(String, index=True, nullable=False)
    year: Column = Column(Integer, nullable=True)  # Year is now optional
    
    def __repr__(self) -> str:
        """
        String representation of Book object.
        
        Returns:
            str: Formatted string with book details
        """
        year_str: str = f", year={self.year}" if self.year else ", year=not specified"
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}'{year_str})>"