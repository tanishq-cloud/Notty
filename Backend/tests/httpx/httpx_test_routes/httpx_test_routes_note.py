import asyncio
import httpx
from fastapi import status
from schemas.user import UserCreateDTO, RefreshTokenDTO
from schemas.note import NoteCreateDTO

from httpx_test_routes_user import login_and_get_tokens,register_user,refresh_access_token

BASE_URL = "http://192.168.0.193:8000"

TEST_USER = {
    "username": "testuser2",
    "password": "testpassword",
    "full_name": "Test User"
}

def get_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}


async def create_note(client, access_token):
    """Test creating a note."""
    print("\nTesting Create Note...")
    response = await client.post(
        "/note/",
        json=NoteCreateDTO(title="Test Note", body="This is a test note.").dict(),
        headers=get_headers(access_token)
    )
    assert response.status_code == status.HTTP_200_OK, f"Failed to create note, got {response.status_code}"
    note = response.json()
    assert "note_id" in note, "Note ID not found in response"
    print("Create Note Response:", note)
    return note["note_id"]

async def get_all_notes(client, access_token):
    """Test fetching all notes."""
    print("\nTesting Get All Notes...")
    response = await client.get("/note/all", headers=get_headers(access_token))
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch notes, got {response.status_code}"
    notes = response.json()
    print("Get All Notes Response:", notes)

async def get_note_by_id(client, access_token, note_id):
    """Test fetching a specific note by ID."""
    print("\nTesting Get Note by ID...")
    response = await client.get(f"/note/{note_id}", headers=get_headers(access_token))
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch note, got {response.status_code}"
    note = response.json()
    print("Get Note Response:", note)

async def update_note(client, access_token, note_id):
    """Test updating a note."""
    print("\nTesting Update Note...")
    response = await client.put(
        f"/note/{note_id}",
        json=NoteCreateDTO(title="Updated Title", body="Updated body.").dict(),
        headers=get_headers(access_token)
    )
    assert response.status_code == status.HTTP_200_OK, f"Failed to update note, got {response.status_code}"
    updated_note = response.json()
    print("Update Note Response:", updated_note)

async def delete_note(client, access_token, note_id):
    """Test deleting a note."""
    print("\nTesting Delete Note...")
    response = await client.delete(f"/note/{note_id}", headers=get_headers(access_token))
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Failed to delete note, got {response.status_code}"
    print("Delete Note Response:", response.text)

async def run_tests():
    """Run all tests sequentially."""
    try:
        # await register_user()

        tokens = await login_and_get_tokens()
        access_token = tokens["access_token"]

        # await refresh_access_token(tokens["refresh_token"])

        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            note_id = await create_note(client, access_token)

            await get_all_notes(client, access_token)

            await get_note_by_id(client, access_token, note_id)

            await update_note(client, access_token, note_id)

            await delete_note(client, access_token, note_id)

        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tests())