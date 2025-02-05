import pytest
from dao.user_dao import UserDAO
from models.model import User
from datetime import timedelta

@pytest.mark.asyncio
async def test_create_user(user_dao: UserDAO):
    """Test creating a new user."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    assert user is not None
    assert user.username == "testuser"
    assert user.full_name == "Test User"


@pytest.mark.asyncio
async def test_get_user_by_username(user_dao: UserDAO):
    """Test retrieving a user by username."""
    # Create a user first
    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    # Retrieve the user
    user = await user_dao.get_user_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_authenticate_user(user_dao: UserDAO):
    """Test authenticating a user."""
    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    user = await user_dao.authenticate_user(username="testuser", password="testpassword")
    assert user is not None
    assert user.username == "testuser"

    invalid_user = await user_dao.authenticate_user(username="testuser", password="wrongpassword")
    assert invalid_user is None


@pytest.mark.asyncio
async def test_create_access_token(user_dao: UserDAO):
    """Test creating an access token."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    token = user_dao.create_access_token(data={"sub": user.username})
    assert token is not None

    payload = user_dao.decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "testuser"


@pytest.mark.asyncio
async def test_create_refresh_token(user_dao: UserDAO):
    """Test creating a refresh token."""
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    token = user_dao.create_refresh_token(data={"sub": user.username})
    assert token is not None

    payload = user_dao.verify_refresh_token(token)
    assert payload is not None
    assert payload.get("sub") == "testuser"