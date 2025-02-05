import pytest
from dao.note_dao import NoteDAO
from models.model import Note, User
from dao.user_dao import UserDAO

@pytest.mark.asyncio
async def test_create_note(note_dao: NoteDAO, user_dao: UserDAO):
    """Test creating a new note."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    assert user is not None

    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=user.id)
    assert note is not None
    assert note.title == "Test Note"
    assert note.body == "This is a test note."
    assert note.user_id == user.id


@pytest.mark.asyncio
async def test_get_note_by_id(note_dao: NoteDAO, user_dao: UserDAO):
    """Test retrieving a note by ID."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=user.id)

    retrieved_note = await note_dao.get_note_by_id(note_id=note.note_id)
    assert retrieved_note is not None
    assert retrieved_note.title == "Test Note"
    assert retrieved_note.body == "This is a test note."


@pytest.mark.asyncio
async def test_get_notes_by_user(note_dao: NoteDAO, user_dao: UserDAO):
    """Test retrieving all notes for a user."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    await note_dao.create_note(title="Note 1", body="Body 1", user_id=user.id)
    await note_dao.create_note(title="Note 2", body="Body 2", user_id=user.id)

    notes = await note_dao.get_notes_by_user(user_id=user.id)
    assert len(notes) == 2
    assert notes[0].title == "Note 1"
    assert notes[1].title == "Note 2"


@pytest.mark.asyncio
async def test_update_note(note_dao: NoteDAO, user_dao: UserDAO):
    """Test updating a note."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=user.id)

    updated_note = await note_dao.update_note(note_id=note.note_id, title="Updated Title", body="Updated Body")
    assert updated_note is not None
    assert updated_note.title == "Updated Title"
    assert updated_note.body == "Updated Body"


@pytest.mark.asyncio
async def test_delete_note(note_dao: NoteDAO, user_dao: UserDAO):
    """Test deleting a note."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    note = await note_dao.create_note(title="Test Note", body="This is a test note.", user_id=user.id)

    deleted_note = await note_dao.delete_note(note_id=note.note_id)
    assert deleted_note is not None
    assert deleted_note.note_id == note.note_id

    retrieved_note = await note_dao.get_note_by_id(note_id=note.note_id)
    assert retrieved_note is None