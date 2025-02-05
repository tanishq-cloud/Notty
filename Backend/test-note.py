import asyncio
import httpx
from fastapi import status
from schemas.note import NoteCreateDTO

# Base URL of the FastAPI app (replace with your actual host)
BASE_URL = "http://127.0.0.1:8000"

# Test user credentials (assumes the user is already registered and logged in)
TEST_USER = {
    "username": "testuser",
    "password": "testpassword"
}

# Test note data
TEST_NOTE = {
    "title": "Test Note",
    "body": "This is a test note."
}

# Helper function to get an access token
async def get_access_token(client):
    """Authenticate the test user and retrieve an access token."""
    response = await client.post(
        "/token/",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    return tokens["access_token"]

# Test creating a note
async def create_note(client, access_token):
    """Test creating a new note."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/note/",
        json=NoteCreateDTO(**TEST_NOTE).dict(),
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    created_note = response.json()
    assert created_note["title"] == TEST_NOTE["title"]
    assert created_note["body"] == TEST_NOTE["body"]
    return created_note["note_id"]

# Test fetching all notes
async def get_all_notes(client, access_token):
    """Test fetching all notes for the current user."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/note/all", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    notes = response.json()
    assert isinstance(notes, list)
    if notes:
        note = notes[0]
        assert note["title"] == TEST_NOTE["title"]
        assert note["body"] == TEST_NOTE["body"]

# Test fetching a single note by ID
async def get_note_by_id(client, access_token, note_id):
    """Test fetching a note by its ID."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"/note/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    note = response.json()
    assert note["title"] == TEST_NOTE["title"]
    assert note["body"] == TEST_NOTE["body"]

# Test updating a note
async def update_note(client, access_token, note_id):
    """Test updating a note's title and body."""
    updated_note_data = {
        "title": "Updated Test Note",
        "body": "This note has been updated."
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.put(
        f"/note/{note_id}",
        json=updated_note_data,
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    updated_note = response.json()
    assert updated_note["title"] == updated_note_data["title"]
    assert updated_note["body"] == updated_note_data["body"]

# Test deleting a note
async def delete_note(client, access_token, note_id):
    """Test deleting a note by its ID."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.delete(f"/note/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Run all tests sequentially
async def run_tests():
    """Run all tests for the note management API."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            # Step 1: Authenticate the test user and get an access token
            access_token = await get_access_token(client)

            # Step 2: Create a new note
            note_id = await create_note(client, access_token)

            # Step 3: Fetch all notes
            await get_all_notes(client, access_token)

            # Step 4: Fetch the note by ID
            await get_note_by_id(client, access_token, note_id)

            # Step 5: Update the note
            await update_note(client, access_token, note_id)

            # Step 6: Delete the note
            await delete_note(client, access_token, note_id)

            print("All tests passed!")
        except AssertionError as e:
            print(f"Test failed: {e}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tests())