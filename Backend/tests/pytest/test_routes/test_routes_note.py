import pytest
from fastapi.testclient import TestClient
from schemas.note import NoteCreateDTO

@pytest.mark.asyncio
async def test_create_note(setup_db: TestClient, authenticated_user, note_dao):
    """Test creating a new note."""
    note_data = NoteCreateDTO(title="Test Note", body="This is a test note.")

    response = setup_db.post(
        "/note/",
        json=note_data.dict(),
        headers={"Authorization": f"Bearer {authenticated_user['access_token']}"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == note_data.title
    assert response_data["body"] == note_data.body
    assert response_data["user_id"] == authenticated_user["user"].id

    note = await note_dao.get_note_by_id(response_data["note_id"])
    assert note is not None
    assert note.title == note_data.title
    assert note.body == note_data.body


@pytest.mark.asyncio
async def test_get_notes(setup_db: TestClient, authenticated_user, note_dao):
    """Test fetching all notes for the current user."""
    note1 = await note_dao.create_note(title="Note 1", body="Body 1", user_id=authenticated_user["user"].id)
    note2 = await note_dao.create_note(title="Note 2", body="Body 2", user_id=authenticated_user["user"].id)

    response = setup_db.get(
        "/note/all",
        headers={"Authorization": f"Bearer {authenticated_user['access_token']}"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]["title"] == "Note 1"
    assert response_data[1]["title"] == "Note 2"


@pytest.mark.asyncio
async def test_get_note_by_id(setup_db: TestClient, authenticated_user, note_dao):
    """Test fetching a note by its ID."""
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=authenticated_user["user"].id)

    response = setup_db.get(
        f"/note/{note.note_id}",
        headers={"Authorization": f"Bearer {authenticated_user['access_token']}"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Note"
    assert response_data["body"] == "This is a test note."


@pytest.mark.asyncio
async def test_update_note(setup_db: TestClient, authenticated_user, note_dao):
    """Test updating a note."""
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=authenticated_user["user"].id)

    updated_note_data = NoteCreateDTO(title="Updated Title", body="Updated Body")

    response = setup_db.put(
        f"/note/{note.note_id}",
        json=updated_note_data.dict(),
        headers={"Authorization": f"Bearer {authenticated_user['access_token']}"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == updated_note_data.title
    assert response_data["body"] == updated_note_data.body


@pytest.mark.asyncio
async def test_delete_note(setup_db: TestClient, authenticated_user, note_dao):
    """Test deleting a note."""
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=authenticated_user["user"].id)

    response = setup_db.delete(
        f"/note/{note.note_id}",
        headers={"Authorization": f"Bearer {authenticated_user['access_token']}"}
    )

    assert response.status_code == 204

    deleted_note = await note_dao.get_note_by_id(note.note_id)
    assert deleted_note is None


