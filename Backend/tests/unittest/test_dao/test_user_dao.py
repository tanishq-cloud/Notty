import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt  
from models.model import User 
from dao.user_dao import UserDAO, get_current_user 

# Constants for testing
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpassword"
TEST_FULL_NAME = "Test User"
TEST_SECRET_KEY = "mysecretkey"
TEST_REFRESH_SECRET_KEY = "Notes_Batman"

class TestUserDAO(unittest.TestCase):
    def setUp(self):
        """Set up a mock session and UserDAO instance for testing."""
        self.mock_db = MagicMock(spec=Session)
        self.user_dao = UserDAO(db=self.mock_db)

    @patch("dao.user_dao.CryptContext.hash")
    async def test_create_user_success(self, mock_hash):
        """Test creating a user successfully."""
        mock_hash.return_value = "hashed_password"
        mock_user = MagicMock()
        self.mock_db.add.return_value = None
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        result = await self.user_dao.create_user(TEST_USERNAME, TEST_PASSWORD, TEST_FULL_NAME)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.assertEqual(result.username, TEST_USERNAME)
        self.assertEqual(result.hashed_password, "hashed_password")

    @patch("dao.user_dao.CryptContext.hash")
    async def test_create_user_duplicate(self, mock_hash):
        """Test creating a user with a duplicate username."""
        mock_hash.return_value = "hashed_password"
        self.mock_db.commit.side_effect = IntegrityError("Duplicate entry", params=None, orig=None)
        result = await self.user_dao.create_user(TEST_USERNAME, TEST_PASSWORD, TEST_FULL_NAME)
        self.assertIsNone(result)
        self.mock_db.rollback.assert_called_once()

    @patch("dao.user_dao.select")
    async def test_get_user_by_username_found(self, mock_select):
        """Test retrieving a user by username when the user exists."""
        mock_user = User(username=TEST_USERNAME, hashed_password="hashed_password", full_name=TEST_FULL_NAME)
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = mock_user
        self.mock_db.execute.return_value = mock_result
        result = await self.user_dao.get_user_by_username(TEST_USERNAME)
        self.mock_db.execute.assert_called_once()
        self.assertEqual(result.username, TEST_USERNAME)
        self.assertEqual(result.full_name, TEST_FULL_NAME)

    @patch("dao.user_dao.select")
    async def test_get_user_by_username_not_found(self, mock_select):
        """Test retrieving a user by username when the user does not exist."""
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = None
        self.mock_db.execute.return_value = mock_result
        result = await self.user_dao.get_user_by_username(TEST_USERNAME)
        self.assertIsNone(result)

    @patch("dao.user_dao.CryptContext.verify")
    async def test_authenticate_user_success(self, mock_verify):
        """Test authenticating a user successfully."""
        mock_verify.return_value = True
        mock_user = User(username=TEST_USERNAME, hashed_password="hashed_password", full_name=TEST_FULL_NAME)
        self.user_dao.get_user_by_username = AsyncMock(return_value=mock_user)
        result = await self.user_dao.authenticate_user(TEST_USERNAME, TEST_PASSWORD)
        self.assertEqual(result.username, TEST_USERNAME)
        self.assertEqual(result.full_name, TEST_FULL_NAME)

    @patch("dao.user_dao.CryptContext.verify")
    async def test_authenticate_user_invalid_credentials(self, mock_verify):
        """Test authenticating a user with invalid credentials."""
        mock_verify.return_value = False
        self.user_dao.get_user_by_username = AsyncMock(return_value=None)
        result = await self.user_dao.authenticate_user(TEST_USERNAME, TEST_PASSWORD)
        self.assertIsNone(result)

    def test_create_access_token(self):
        """Test creating an access token."""
        data = {"sub": TEST_USERNAME}
        token = self.user_dao.create_access_token(data)
        self.assertIsNotNone(token)
        payload = self.user_dao.decode_access_token(token)
        self.assertEqual(payload["sub"], TEST_USERNAME)
        self.assertIn("exp", payload)

    def test_decode_access_token_expired(self):
        """Test decoding an expired access token."""
        expired_data = {"sub": TEST_USERNAME, "exp": datetime.utcnow() - timedelta(minutes=10)}
        expired_token = jwt.encode(expired_data, TEST_SECRET_KEY, algorithm="HS256")
        result = self.user_dao.decode_access_token(expired_token)
        self.assertIsNone(result)

    def test_create_refresh_token(self):
        """Test creating a refresh token."""
        data = {"sub": TEST_USERNAME}
        token = self.user_dao.create_refresh_token(data)
        self.assertIsNotNone(token)
        payload = jwt.decode(token, TEST_REFRESH_SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(payload["sub"], TEST_USERNAME)
        self.assertIn("exp", payload)

    def test_verify_refresh_token_success(self):
        """Test verifying a valid refresh token."""
        data = {"sub": TEST_USERNAME, "exp": datetime.utcnow() + timedelta(days=1)}
        token = jwt.encode(data, TEST_REFRESH_SECRET_KEY, algorithm="HS256")
        result = self.user_dao.verify_refresh_token(token)
        self.assertEqual(result["sub"], TEST_USERNAME)

    def test_verify_refresh_token_expired(self):
        """Test verifying an expired refresh token."""
        expired_data = {"sub": TEST_USERNAME, "exp": datetime.utcnow() - timedelta(days=1)}
        expired_token = jwt.encode(expired_data, TEST_REFRESH_SECRET_KEY, algorithm="HS256")
        with self.assertRaises(HTTPException) as context:
            self.user_dao.verify_refresh_token(expired_token)
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Refresh token expired")

    @patch("dao.user_dao.UserDAO.decode_access_token")
    @patch("dao.user_dao.UserDAO.get_user_by_username")
    async def test_get_current_user_success(self, mock_get_user, mock_decode_token):
        """Test fetching the current user with a valid token."""
        mock_decode_token.return_value = {"sub": TEST_USERNAME}
        mock_user = User(username=TEST_USERNAME, hashed_password="hashed_password", full_name=TEST_FULL_NAME)
        mock_get_user.return_value = mock_user
        result = await get_current_user("valid_token", self.mock_db)
        self.assertEqual(result.username, TEST_USERNAME)
        self.assertEqual(result.full_name, TEST_FULL_NAME)

    @patch("dao.user_dao.UserDAO.decode_access_token")
    async def test_get_current_user_invalid_token(self, mock_decode_token):
        """Test fetching the current user with an invalid token."""
        mock_decode_token.return_value = None
        with self.assertRaises(HTTPException) as context:
            await get_current_user("invalid_token", self.mock_db)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid or expired token")

if __name__ == "__main__":
    unittest.main()