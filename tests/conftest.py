import pytest
from httpx import AsyncClient
from app import app  # Adjust this based on your actual module structure
from app.database import init_db  # Import your init_db function
from app.models import User, Book, Review  # Ensure these are defined
from sqlalchemy.ext.asyncio import create_async_engine

# Use an SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
async def test_app():
    app.config.update({
        "TESTING": True,
        "DATABASE_URL": DATABASE_URL,
        "SECRET_KEY": "test_secret_key"
    })

    print("Using DATABASE_URL:", app.config["DATABASE_URL"])  # Debugging line

    # Create an asynchronous engine for SQLite
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)

    # Set up the database
    async with engine.begin() as conn:
        await conn.run_sync(init_db)  # Initialize your database

    yield app  # This will be used in your tests

    # Optional: Teardown database
    async with engine.begin() as conn:
        await conn.run_sync(User.__table__.drop)
        await conn.run_sync(Book.__table__.drop)
        await conn.run_sync(Review.__table__.drop)

@pytest.fixture(scope="function")
async def client(test_app):
    # Create a test client for your app
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def access_token(client):
    # Register a user
    response = await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201

    # Login and get the access token
    response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = await response.json()
    assert response.status_code == 200
    assert 'token' in data
    return data['token']  # Return the token for use in other tests
