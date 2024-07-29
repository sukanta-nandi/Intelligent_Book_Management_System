import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://admin:admin1234@book-system-postgres/books_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
