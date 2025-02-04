import pytest
import jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from dao.user_dao import UserDAO, SECRET_KEY, ALGORITHM, REFRESH_SECRET_KEY
from models.model import User

@pytest.mark.asyncio
async def test_create_user(override_get_db: AsyncSession):
    """Test user creation"""
    db = override_get_db
    user_dao = UserDAO(db)

    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    assert user is not None
    assert user.username == "testuser"

@pytest.mark.asyncio
async def test_get_user_by_username(override_get_db: AsyncSession):
    """Test retrieving user by username"""
    db = override_get_db
    user_dao = UserDAO(db)

    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    user = await user_dao.get_user_by_username("testuser")

    assert user is not None
    assert user.username == "testuser"

@pytest.mark.asyncio
async def test_authenticate_user(override_get_db: AsyncSession):
    """Test user authentication"""
    db = override_get_db
    user_dao = UserDAO(db)

    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    authenticated_user = await user_dao.authenticate_user("testuser", "testpassword")

    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"

@pytest.mark.asyncio
async def test_authenticate_user_fail(override_get_db: AsyncSession):
    """Test failed authentication"""
    db = override_get_db
    user_dao = UserDAO(db)

    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    authenticated_user = await user_dao.authenticate_user("testuser", "wrongpassword")

    assert authenticated_user is None

def test_create_access_token():
    """Test access token generation"""
    user_dao = UserDAO(None)  # No DB required

    token = user_dao.create_access_token({"sub": "testuser"})
    
    assert token is not None
    assert isinstance(token, str)

def test_decode_access_token():
    """Test decoding a valid access token"""
    user_dao = UserDAO(None)
    
    data = {"sub": "testuser"}
    token = user_dao.create_access_token(data)
    
    decoded_data = user_dao.decode_access_token(token)
    
    assert decoded_data is not None
    assert decoded_data["sub"] == "testuser"

def test_decode_invalid_access_token():
    """Test decoding an invalid access token"""
    user_dao = UserDAO(None)
    
    invalid_token = "invalid.token.string"
    decoded_data = user_dao.decode_access_token(invalid_token)

    assert decoded_data is None

def test_create_refresh_token():
    """Test refresh token generation"""
    user_dao = UserDAO(None)

    token = user_dao.create_refresh_token({"sub": "testuser"})
    
    assert token is not None
    assert isinstance(token, str)

def test_verify_valid_refresh_token():
    """Test decoding a valid refresh token"""
    user_dao = UserDAO(None)

    data = {"sub": "testuser"}
    token = user_dao.create_refresh_token(data)
    
    decoded_data = user_dao.verify_refresh_token(token)

    assert decoded_data is not None
    assert decoded_data["sub"] == "testuser"

def test_verify_invalid_refresh_token():
    """Test verifying an invalid refresh token"""
    user_dao = UserDAO(None)

    invalid_token = "invalid.refresh.token"
    
    with pytest.raises(Exception):
        user_dao.verify_refresh_token(invalid_token)

@pytest.mark.asyncio
async def test_get_current_user(override_get_db: AsyncSession):
    """Test fetching current user from token"""
    db = override_get_db
    user_dao = UserDAO(db)

    # Create a user
    await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")

    # Generate a valid token
    token = user_dao.create_access_token({"sub": "testuser"})

    # Fetch user using token
    fetched_user = await user_dao.get_user_by_username("testuser")

    assert fetched_user is not None
    assert fetched_user.username == "testuser"
