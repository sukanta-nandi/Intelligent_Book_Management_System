# Intelligent_Book_Management_System

## Description

Intelligent_Book_Management_System is a RESTful API built with Quart and SQLAlchemy for managing books and their reviews. It includes user authentication with token-based authentication using JWT.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sukanta-nandi/Intelligent_Book_Management_System.git
   cd Intelligent_Book_Management_System
   ```

2. Create a `.env` file in the root directory and add the following content:
   ```env
   DATABASE_URL=postgresql+asyncpg://admin:admin1234@book-system-postgres:5432/books_db
   SECRET_KEY=your_secret_key
   ```

3. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   docker-compose up -d
   ```

4. **Access the application**:
   - **API**: [http://localhost:5000](http://localhost:5000)
   - **pgAdmin**: [http://localhost:8080](http://localhost:8080) (default email: `admin@admin.com`, default password: `admin`)

### Using the API

#### Register a new user
```bash
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
```

#### Login
```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
```

#### Add a new book
```bash
curl -X POST http://localhost:5000/books -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"title": "Sample Book", "author": "Author Name", "genre": "Fiction", "year_published": 2020, "summary": "This is a sample book."}'
```

#### Get all books
```bash
curl -X GET http://localhost:5000/books -H "Authorization: Bearer <your_token>"
```

#### Get a book by ID
```bash
curl -X GET http://localhost:5000/books/1 -H "Authorization: Bearer <your_token>"
```

#### Update a book by ID
```bash
curl -X PUT http://localhost:5000/books/1 -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"title": "Updated Book Title"}'
```

#### Delete a book by ID
```bash
curl -X DELETE http://localhost:5000/books/1 -H "Authorization: Bearer <your_token>"
```

#### Add a review for a book
```bash
curl -X POST http://localhost:5000/books/1/reviews -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"user_id": 1, "review_text": "Great book!", "rating": 5}'
```

#### Get all reviews for a book
```bash
curl -X GET http://localhost:5000/books/1/reviews -H "Authorization: Bearer <your_token>"
```

#### Get a summary and aggregated rating for a book
```bash
curl -X GET http://localhost:5000/books/1/summary -H "Authorization: Bearer <your_token>"
```

## Project Structure
```
Intelligent_Book_Management_System/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── review.py
│   └── schemas.py
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── .dockerignore
└── run.py
```

## License
This project is licensed under the MIT License.
