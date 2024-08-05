import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(test_app):  # Using the test_app fixture
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        response = await client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 201

@pytest.mark.asyncio
async def test_login(test_app):  # Using the test_app fixture
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        # First, register the user
        await client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Now, attempt to login
        response = await client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        data = response.json()
        assert response.status_code == 200
        assert 'token' in data

@pytest.mark.asyncio
async def test_login_invalid_credentials(test_app):  # Using the test_app fixture
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        response = await client.post('/login', json={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        data = response.json()
        assert data['message'] == 'Invalid credentials'
