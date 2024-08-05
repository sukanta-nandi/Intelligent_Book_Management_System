import pytest
from httpx import AsyncClient
from app import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_book(client, access_token):
    response = await client.post('/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Fiction',
        'year_published': 2021,
        'summary': 'This is a test book.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Test Book'

@pytest.mark.asyncio
async def test_get_books(client):
    response = await client.get('/books')
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_book(client, access_token):
    # First, create a book to delete
    create_response = await client.post('/books', json={
        'title': 'Book to delete',
        'author': 'Author',
        'genre': 'Fiction',
        'year_published': 2021,
        'summary': 'This book will be deleted.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    book_id = create_response.json()['id']
    
    # Now delete the book
    delete_response = await client.delete(f'/books/{book_id}', headers={'Authorization': f'Bearer {access_token}'})
    
    assert delete_response.status_code == 204
