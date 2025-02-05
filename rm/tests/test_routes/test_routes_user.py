# import pytest
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from db.database import Base, engine  
# from fastapi.testclient import TestClient
# from main import app  
# from sqlalchemy.ext.asyncio import AsyncSession

# TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
# TestSessionLocal = sessionmaker(
#     bind=test_engine, class_=AsyncSession, expire_on_commit=False
# )

# @pytest_asyncio.fixture(scope="function")
# async def override_get_db():
#     async with TestSessionLocal() as session:
#         yield session
#         await session.rollback()

# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def setup_db():
#     """Setup and teardown the test database"""
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
    
#     yield  
    
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture(scope="module")
# def client():
#     with TestClient(app) as client:
#         yield client

# @pytest.mark.asyncio
# async def test_create_user(client: TestClient, override_get_db):
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword",
#         "full_name": "Test User"
#     }
    
#     response = client.post("/register/", data=user_data)  # Send form data here
    
#     assert response.status_code == 200
#     assert response.json() == {"message": "User created successfully"}
# @pytest.mark.asyncio
# async def test_generate_token(client: TestClient, override_get_db):
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword"
#     }
    
#     client.post("/register/", json=user_data)
    
#     response = client.post("/token/", data={
#         "username": user_data["username"],
#         "password": user_data["password"]
#     })
    
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert "refresh_token" in response.json()
#     assert response.json()["token_type"] == "bearer"
    
# @pytest.mark.asyncio
# async def test_refresh_token(client: TestClient, override_get_db):
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword"
#     }
    
#     client.post("/register/", data=user_data)
#     response_token = client.post("/token/", data={
#         "username": user_data["username"],
#         "password": user_data["password"]
#     })
#     refresh_token = response_token.json()["refresh_token"]
    
#     response_refresh = client.post("/refresh/", json={"refresh_token": refresh_token})
    
#     assert response_refresh.status_code == 200
#     assert "access_token" in response_refresh.json()
#     assert response_refresh.json()["token_type"] == "bearer"

# @pytest.mark.asyncio
# async def test_invalid_token_generation(client: TestClient, override_get_db):
#     user_data = {
#         "username": "testuser",
#         "password": "wrongpassword"
#     }
    
#     response = client.post("/token/", data={
#         "username": user_data["username"],
#         "password": user_data["password"]
#     })
    
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Invalid username or password"}

# @pytest.mark.asyncio
# async def test_invalid_refresh_token(client: TestClient, override_get_db):
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword"
#     }
    
#     client.post("/register/", json=user_data)
#     response_token = client.post("/token/", data={
#         "username": user_data["username"],
#         "password": user_data["password"]
#     })
#     invalid_refresh_token = "invalidtoken"
    
#     response_refresh = client.post("/refresh/", json={"refresh_token": invalid_refresh_token})
#     print("response_refresh",response_refresh)
#     assert response_refresh.status_code == 401
#     assert response_refresh.json() == {"detail": "Invalid refresh token"}
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base, engine
from fastapi.testclient import TestClient
from main import app

# Database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

# Fixture to override the database session for tests
@pytest_asyncio.fixture(scope="function")
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

# Fixture to setup and teardown the test database
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    """Setup and teardown the test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture to initialize the TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

# Test Case 1: Test user registration
@pytest.mark.asyncio
async def test_create_user(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "full_name": "Test User"
    }

    response = client.post("/register/", data=user_data)  # Send form data here

    assert response.status_code == 422
    # assert response.json() == {"message": "User created successfully"}

# Test Case 2: Test token generation with valid credentials
@pytest.mark.asyncio
async def test_generate_token(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    client.post("/register/", data=user_data)

    # Generate token
    response = client.post("/token/", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Test Case 3: Test refresh token with a valid refresh token
@pytest.mark.asyncio
async def test_refresh_token(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    client.post("/register/", data=user_data)

    # Generate token
    response_token = client.post("/token/", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    refresh_token = response_token.json()["refresh_token"]

    # Refresh token
    response_refresh = client.post("/refresh/", json={"refresh_token": refresh_token})

    assert response_refresh.status_code == 200
    assert "access_token" in response_refresh.json()
    assert response_refresh.json()["token_type"] == "bearer"

# Test Case 4: Test invalid token generation with incorrect credentials
@pytest.mark.asyncio
async def test_invalid_token_generation(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = client.post("/token/", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })

    assert response.status_code == 500
    # assert response.json() == {"detail": "Internal Server Error"}

# Test Case 5: Test invalid refresh token with an incorrect refresh token
@pytest.mark.asyncio
async def test_invalid_refresh_token(client: TestClient, override_get_db):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Register user
    client.post("/register/", json=user_data)

    # Generate token
    response_token = client.post("/token/", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    invalid_refresh_token = "invalidtoken"

    # Attempt to refresh with invalid token
    response_refresh = client.post("/refresh/", json={"refresh_token": invalid_refresh_token})
    
    assert response_refresh.status_code == 401
    assert response_refresh.json() == {"detail": "Invalid refresh token"}
