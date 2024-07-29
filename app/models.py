from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    genre = Column(String(100))
    year_published = Column(Integer)
    summary = Column(Text)
    reviews = relationship('Review', back_populates='book', cascade='all, delete-orphan')

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    book = relationship('Book', back_populates='reviews')
