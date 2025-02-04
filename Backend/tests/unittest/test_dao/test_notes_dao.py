import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.orm import Session
from models.model import Note 
from dao.note_dao import NoteDAO  

# Constants for testing
TEST_TITLE = "Test Note"
TEST_BODY = "This is a test note."
TEST_USER_ID = 1
TEST_NOTE_ID = 123


class TestNoteDAO(unittest.TestCase):
    def setUp(self):
        """Set up a mock session and NoteDAO instance for testing."""
        self.mock_db = MagicMock(spec=Session)
        self.note_dao = NoteDAO(db=self.mock_db)

    @patch("dao.note_dao.select")
    async def test_create_note_success(self, mock_select):
        """Test creating a note successfully."""
        mock_note = MagicMock()
        mock_note.note_id = TEST_NOTE_ID
        mock_note.title = TEST_TITLE
        mock_note.body = TEST_BODY
        mock_note.user_id = TEST_USER_ID

        self.mock_db.add.return_value = None
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()

        result = await self.note_dao.create_note(TEST_TITLE, TEST_BODY, TEST_USER_ID)

        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.assertEqual(result.title, TEST_TITLE)
        self.assertEqual(result.body, TEST_BODY)
        self.assertEqual(result.user_id, TEST_USER_ID)

    @patch("dao.note_dao.select")
    async def test_get_note_by_id_found(self, mock_select):
        """Test retrieving a note by ID when the note exists."""
        mock_note = Note(note_id=TEST_NOTE_ID, title=TEST_TITLE, body=TEST_BODY, user_id=TEST_USER_ID)
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = mock_note
        self.mock_db.execute.return_value = mock_result

        result = await self.note_dao.get_note_by_id(TEST_NOTE_ID)

        self.mock_db.execute.assert_called_once()
        self.assertEqual(result.note_id, TEST_NOTE_ID)
        self.assertEqual(result.title, TEST_TITLE)
        self.assertEqual(result.body, TEST_BODY)

    @patch("dao.note_dao.select")
    async def test_get_note_by_id_not_found(self, mock_select):
        """Test retrieving a note by ID when the note does not exist."""
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = None
        self.mock_db.execute.return_value = mock_result

        result = await self.note_dao.get_note_by_id(TEST_NOTE_ID)

        self.assertIsNone(result)

    @patch("dao.note_dao.select")
    async def test_get_notes_by_user_found(self, mock_select):
        """Test retrieving all notes for a user when notes exist."""
        mock_notes = [
            Note(note_id=1, title="Note 1", body="Body 1", user_id=TEST_USER_ID),
            Note(note_id=2, title="Note 2", body="Body 2", user_id=TEST_USER_ID),
        ]
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_notes
        self.mock_db.execute.return_value = mock_result

        result = await self.note_dao.get_notes_by_user(TEST_USER_ID)

        self.mock_db.execute.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Note 1")
        self.assertEqual(result[1].title, "Note 2")

    @patch("dao.note_dao.select")
    async def test_get_notes_by_user_not_found(self, mock_select):
        """Test retrieving all notes for a user when no notes exist."""
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        self.mock_db.execute.return_value = mock_result

        result = await self.note_dao.get_notes_by_user(TEST_USER_ID)

        self.assertEqual(len(result), 0)

    @patch("dao.note_dao.NoteDAO.get_note_by_id")
    async def test_update_note_success(self, mock_get_note_by_id):
        """Test updating a note successfully."""
        mock_note = Note(note_id=TEST_NOTE_ID, title=TEST_TITLE, body=TEST_BODY, user_id=TEST_USER_ID)
        mock_get_note_by_id.return_value = mock_note

        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()

        result = await self.note_dao.update_note(TEST_NOTE_ID, "Updated Title", "Updated Body")

        mock_get_note_by_id.assert_called_once_with(TEST_NOTE_ID)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.assertEqual(result.title, "Updated Title")
        self.assertEqual(result.body, "Updated Body")

    @patch("dao.note_dao.NoteDAO.get_note_by_id")
    async def test_update_note_not_found(self, mock_get_note_by_id):
        """Test updating a note that does not exist."""
        mock_get_note_by_id.return_value = None

        result = await self.note_dao.update_note(TEST_NOTE_ID, "Updated Title", "Updated Body")

        mock_get_note_by_id.assert_called_once_with(TEST_NOTE_ID)
        self.assertIsNone(result)

    @patch("dao.note_dao.NoteDAO.get_note_by_id")
    async def test_delete_note_success(self, mock_get_note_by_id):
        """Test deleting a note successfully."""
        mock_note = Note(note_id=TEST_NOTE_ID, title=TEST_TITLE, body=TEST_BODY, user_id=TEST_USER_ID)
        mock_get_note_by_id.return_value = mock_note

        self.mock_db.delete.return_value = None
        self.mock_db.commit = AsyncMock()

        result = await self.note_dao.delete_note(TEST_NOTE_ID)

        mock_get_note_by_id.assert_called_once_with(TEST_NOTE_ID)
        self.mock_db.delete.assert_called_once_with(mock_note)
        self.mock_db.commit.assert_called_once()
        self.assertEqual(result.note_id, TEST_NOTE_ID)

    @patch("dao.note_dao.NoteDAO.get_note_by_id")
    async def test_delete_note_not_found(self, mock_get_note_by_id):
        """Test deleting a note that does not exist."""
        mock_get_note_by_id.return_value = None

        result = await self.note_dao.delete_note(TEST_NOTE_ID)

        mock_get_note_by_id.assert_called_once_with(TEST_NOTE_ID)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()