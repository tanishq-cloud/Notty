import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import Note
from dao.note_dao import NoteDAO

@pytest.mark.asyncio
async def test_create_note(override_get_db: AsyncSession):
    """Test creating a new note"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        note = await note_dao.create_note(title="Test Title", body="Test Body", user_id=1)

        assert note is not None
        assert note.title == "Test Title"
        assert note.body == "Test Body"
        assert note.user_id == 1

@pytest.mark.asyncio
async def test_get_note_by_id(override_get_db: AsyncSession):
    """Test retrieving a note by its ID"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        created_note = await note_dao.create_note(title="Test Note", body="Sample Content", user_id=1)
        retrieved_note = await note_dao.get_note_by_id(created_note.note_id)

        assert retrieved_note is not None
        assert retrieved_note.title == "Test Note"
        assert retrieved_note.body == "Sample Content"

@pytest.mark.asyncio
async def test_get_notes_by_user(override_get_db: AsyncSession):
    """Test retrieving all notes for a user"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        await note_dao.create_note(title="Note 1", body="Content 1", user_id=1)
        await note_dao.create_note(title="Note 2", body="Content 2", user_id=1)

        notes = await note_dao.get_notes_by_user(1)

        assert len(notes) == 2
        assert notes[0].title == "Note 1"
        assert notes[1].title == "Note 2"

@pytest.mark.asyncio
async def test_update_note(override_get_db: AsyncSession):
    """Test updating an existing note"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        note = await note_dao.create_note(title="Old Title", body="Old Body", user_id=1)
        updated_note = await note_dao.update_note(note.note_id, title="New Title", body="New Body")

        assert updated_note is not None
        assert updated_note.title == "New Title"
        assert updated_note.body == "New Body"

@pytest.mark.asyncio
async def test_update_non_existent_note(override_get_db: AsyncSession):
    """Test updating a note that doesn't exist"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        updated_note = await note_dao.update_note(note_id=999, title="Updated Title", body="Updated Body")

        assert updated_note is None

@pytest.mark.asyncio
async def test_delete_note(override_get_db: AsyncSession):
    """Test deleting a note"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        note = await note_dao.create_note(title="Delete Me", body="Some Body", user_id=1)
        deleted_note = await note_dao.delete_note(note.note_id)

        assert deleted_note is not None
        # assert deleted_note.note_id == note.note_id

        fetched_note = await note_dao.get_note_by_id(note.note_id)
        assert fetched_note is None

@pytest.mark.asyncio
async def test_delete_non_existent_note(override_get_db: AsyncSession):
    """Test deleting a note that doesn't exist"""
    async with override_get_db as db:
        note_dao = NoteDAO(db)

        deleted_note = await note_dao.delete_note(note_id=999)

        assert deleted_note is None
