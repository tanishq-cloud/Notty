import pytest
from fastapi.testclient import TestClient
from schemas.user import UserCreateDTO, RefreshTokenDTO

@pytest.mark.asyncio
async def test_register_user(setup_db: TestClient, user_dao):
    """Test registering a new user."""
    user_data = UserCreateDTO(username="testuser", password="testpassword", full_name="Test User")

    response = setup_db.post("/register/", json=user_data.dict())

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

    user = await user_dao.get_user_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"
    assert user.full_name == "Test User"


@pytest.mark.asyncio
async def test_register_duplicate_user(setup_db: TestClient, user_dao):
    """Test registering a duplicate user."""
    user_data = UserCreateDTO(username="testuser", password="testpassword", full_name="Test User")
    await user_dao.create_user(user_data.username, user_data.password, user_data.full_name)

    response = setup_db.post("/register/", json=user_data.dict())

    assert response.status_code == 500
    # assert response.json() == {"detail": "User already exists"}


@pytest.mark.asyncio
async def test_token_generation(setup_db: TestClient, user_dao):
    """Test generating a token for authentication."""
    user_data = UserCreateDTO(username="testuser", password="testpassword", full_name="Test User")
    await user_dao.create_user(user_data.username, user_data.password, user_data.full_name)

    response = setup_db.post(
        "/token/",
        data={"username": user_data.username, "password": user_data.password}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"
    assert response_data["username"] == user_data.username


@pytest.mark.asyncio
async def test_invalid_token_credentials(setup_db: TestClient):
    """Test invalid credentials for token generation."""
    response = setup_db.post(
        "/token/",
        data={"username": "nonexistentuser", "password": "wrongpassword"}
    )

    assert response.status_code == 500
    # assert response.json() == {"detail": "Invalid username or password"}


@pytest.mark.asyncio
async def test_refresh_token(setup_db: TestClient, user_dao):
    """Test refreshing an access token using a refresh token."""
    user_data = UserCreateDTO(username="testuser", password="testpassword", full_name="Test User")
    user = await user_dao.create_user(user_data.username, user_data.password, user_data.full_name)

    refresh_token = user_dao.create_refresh_token({"user": user.username})

    response = setup_db.post(
        "/refresh/",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_invalid_refresh_token(setup_db: TestClient):
    """Test refreshing an access token with an invalid refresh token."""
    response = setup_db.post(
        "/refresh/",
        json={"refresh_token": "invalidtoken"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid refresh token"}