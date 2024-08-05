import pytest
from httpx import AsyncClient
from app import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_review(client, access_token):
    # Create a book to review
    book_response = await client.post('/books', json={
        'title': 'Book for Review',
        'author': 'Author',
        'genre': 'Fiction',
        'year_published': 2021,
        'summary': 'This is a test book.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    book_id = book_response.json()['id']
    
    # Now create a review for that book
    review_response = await client.post(f'/books/{book_id}/reviews', json={
        'user_id': 1,  # Assuming user_id is 1 for testing purposes
        'review_text': 'Great book!',
        'rating': 5
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    assert review_response.status_code == 201

@pytest.mark.asyncio
async def test_get_reviews(client):
    book_id = 1  # Assuming there's a book with ID 1
    response = await client.get(f'/books/{book_id}/reviews')
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_book_summary(client, access_token):
    # Create a book to get summary
    book_response = await client.post('/books', json={
        'title': 'Book for Summary',
        'author': 'Author',
        'genre': 'Fiction',
        'year_published': 2021,
        'summary': 'This is a test book for summary.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    book_id = book_response.json()['id']
    
    # Add a review for the book
    await client.post(f'/books/{book_id}/reviews', json={
        'user_id': 1,  # Assuming user_id is 1 for testing purposes
        'review_text': 'Amazing read!',
        'rating': 5
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    # Now get the book summary
    summary_response = await client.get(f'/books/{book_id}/summary')
    
    assert summary_response.status_code == 200
    summary_data = summary_response.json()
    assert summary_data['title'] == 'Book for Summary'
    assert 'review_count' in summary_data
    assert 'average_rating' in summary_data
