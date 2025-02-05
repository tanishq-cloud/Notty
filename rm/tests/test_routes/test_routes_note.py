import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession
from dao import user_dao
from models.model import User
from dao.note_dao import NoteDAO
from schemas.note import NoteCreateDTO, NoteResponseDTO
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Test Fixture for setting up the database session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

# Test Fixture for setting up the client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

# Test Case 1: Test creating a note
@pytest.mark.asyncio
async def test_create_note(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "full_name":"CGS"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200
    
    # Get the user for authorization
    response = client.post("/token/", json=user_data)
    # user = await user1.create_access_token(user_data)

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.access_token}"})

    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]
    assert response.json()["body"] == note_data["body"]

# Test Case 2: Test fetching all notes
@pytest.mark.asyncio
async def test_get_notes(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200
    
    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = [
        {"title": "Test Note 1", "body": "Body of note 1"},
        {"title": "Test Note 2", "body": "Body of note 2"}
    ]
    
    # Create notes
    for note in note_data:
        response = client.post("/note/", json=note, headers={"Authorization": f"Bearer {user.token}"})
        assert response.status_code == 200

    # Fetch all notes
    response = client.get("/note/all", headers={"Authorization": f"Bearer {user.token}"})
    assert response.status_code == 200
    assert len(response.json()) == len(note_data)

# Test Case 3: Test getting a single note by its ID
@pytest.mark.asyncio
async def test_get_note_by_id(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200

    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    # Create note
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.token}"})
    note_id = response.json()["id"]

    # Fetch the created note by ID
    response = client.get(f"/note/{note_id}", headers={"Authorization": f"Bearer {user.token}"})
    assert response.status_code == 200
    assert response.json()["id"] == note_id

# Test Case 4: Test updating a note
@pytest.mark.asyncio
async def test_update_note(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200

    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    # Create note
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.token}"})
    note_id = response.json()["id"]

    # Update note
    updated_note_data = {"title": "Updated Test Note", "body": "This is the updated body"}
    response = client.put(f"/note/{note_id}", json=updated_note_data, headers={"Authorization": f"Bearer {user.token}"})

    assert response.status_code == 200
    assert response.json()["title"] == updated_note_data["title"]
    assert response.json()["body"] == updated_note_data["body"]

# Test Case 5: Test deleting a note
@pytest.mark.asyncio
async def test_delete_note(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200

    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    # Create note
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.token}"})
    note_id = response.json()["id"]

    # Delete note
    response = client.delete(f"/note/{note_id}", headers={"Authorization": f"Bearer {user.token}"})
    assert response.status_code == 204

    # Try fetching the deleted note
    response = client.get(f"/note/{note_id}", headers={"Authorization": f"Bearer {user.token}"})
    assert response.status_code == 404

# Test Case 6: Test unauthorized access to update a note
@pytest.mark.asyncio
async def test_unauthorized_update_note(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200

    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    # Create note
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.token}"})
    note_id = response.json()["id"]

    # Try updating note with another user token (unauthorized)
    another_user_data = {
        "username": "anotheruser",
        "password": "anotherpassword"
    }

    # Register another user
    response = client.post("/register/", data=another_user_data)
    assert response.status_code == 200

    another_user = await user_dao.get_user_by_username(another_user_data["username"])

    updated_note_data = {"title": "Updated Test Note", "body": "This is the updated body"}
    response = client.put(f"/note/{note_id}", json=updated_note_data, headers={"Authorization": f"Bearer {another_user.token}"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to update this note"}

# Test Case 7: Test deleting a note by a non-authorized user
@pytest.mark.asyncio
async def test_unauthorized_delete_note(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    response = client.post("/register/", data=user_data)
    assert response.status_code == 200

    # Get the user for authorization
    user = await user_dao.get_user_by_username(user_data["username"])

    note_data = {
        "title": "Test Note",
        "body": "This is a test note."
    }

    # Create note
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {user.token}"})
    note_id = response.json()["id"]

    # Try deleting note with another user token (unauthorized)
    another_user_data = {
        "username": "anotheruser",
        "password": "anotherpassword"
    }

    # Register another user
    response = client.post("/register/", data=another_user_data)
    assert response.status_code == 200

    another_user = await user_dao.get_user_by_username(another_user_data["username"])

    response = client.delete(f"/note/{note_id}", headers={"Authorization": f"Bearer {another_user.token}"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to delete this note"}
