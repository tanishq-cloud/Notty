import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dao.note_dao import NoteDAO
from dao.user_dao import UserDAO
from models.model import Base, User 
from main import app  
from db.database import get_db  

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def override_get_db():
    """Fixture to provide a fresh test database session per test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    TestingSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def setup_db(override_get_db):
    """Fixture to override the get_db dependency for FastAPI."""
    app.dependency_overrides[get_db] = lambda: override_get_db
    with TestClient(app) as client:
        yield client  


@pytest_asyncio.fixture
async def user_dao(override_get_db):
    """Fixture to provide a UserDAO instance with a test database session."""
    return UserDAO(db=override_get_db)

@pytest_asyncio.fixture
async def note_dao(override_get_db):
    """Fixture to provide a NoteDAO instance with a test database session."""
    return NoteDAO(db=override_get_db)


@pytest_asyncio.fixture
async def authenticated_user(setup_db, user_dao):
    """Fixture to create an authenticated user and generate an access token."""
    # Create a user
    user = await user_dao.create_user(username="testuser", password="testpassword", full_name="Test User")
    assert user is not None

    # Generate an access token
    token = user_dao.create_access_token(data={"sub": user.username})
    return {"user": user, "access_token": token}