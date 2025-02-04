import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import status
import asyncio

# Adjust these imports based on your project structure
from main import app
from db.database import get_db
from models.model import Base

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def authenticated_client(client):
    # Register user
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "full_name": "CGS"
    }
    response = client.post("/register/", json=user_data)  # Note: using json parameter
    assert response.status_code == 200

    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/token/", data=login_data)  # Note: using data for form data
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return client, headers

@pytest.mark.asyncio
async def test_create_note(client: TestClient, override_get_db):
    # Register user
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "full_name": "CGS"
    }
    response = client.post("/register/", json=user_data)  # Changed to json
    assert response.status_code == 200

    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/token/", data=login_data)  # Form data for token endpoint
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create note
    headers = {"Authorization": f"Bearer {token}"}
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]
    assert response.json()["body"] == note_data["body"]

@pytest.mark.asyncio
async def test_get_notes(client: TestClient, authenticated_client):
    client, headers = authenticated_client
    
    # Create a test note first
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers=headers)
    assert response.status_code == 200

    # Get all notes
    response = client.get("/note/all", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == note_data["title"]

@pytest.mark.asyncio
async def test_get_note_by_id(client: TestClient, authenticated_client):
    client, headers = authenticated_client
    
    # Create a test note first
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers=headers)
    assert response.status_code == 200
    note_id = response.json()["id"]

    # Get specific note
    response = client.get(f"/note/{note_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == note_data["title"]

@pytest.mark.asyncio
async def test_update_note(client: TestClient, authenticated_client):
    client, headers = authenticated_client
    
    # Create a test note first
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers=headers)
    assert response.status_code == 200
    note_id = response.json()["id"]

    # Update note
    updated_data = {
        "title": "Updated Title",
        "body": "Updated body"
    }
    response = client.put(f"/note/{note_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["body"] == updated_data["body"]

@pytest.mark.asyncio
async def test_delete_note(client: TestClient, authenticated_client):
    client, headers = authenticated_client
    
    # Create a test note first
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers=headers)
    assert response.status_code == 200
    note_id = response.json()["id"]

    # Delete note
    response = client.delete(f"/note/{note_id}", headers=headers)
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/note/{note_id}", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_unauthorized_access(client: TestClient):
    response = client.get("/note/all")
    assert response.status_code == 401

# Authentication tests
@pytest.mark.asyncio
async def test_register_user(client: TestClient):
    user_data = {
        "username": "newuser",
        "password": "newpassword",
        "full_name": "New User"
    }
    response = client.post("/register/", json=user_data)  # Using json
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

@pytest.mark.asyncio
async def test_login_user(client: TestClient):
    # Register first
    user_data = {
        "username": "loginuser",
        "password": "loginpassword",
        "full_name": "Login User"
    }
    response = client.post("/register/", json=user_data)
    assert response.status_code == 200

    # Then login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword"
    }
    response = client.post("/token/", data=login_data)  # Using data for form
    assert response.status_code == 200
    assert "access_token" in response.json()