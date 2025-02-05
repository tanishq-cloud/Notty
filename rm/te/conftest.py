# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Import your FastAPI app
from db1 import Base, get_db  # Adjust imports based on your project structure

# Fixture for creating an in-memory database
@pytest.fixture(scope="function")
async def test_db():
    # In-memory SQLite for tests
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
    
    yield TestingSessionLocal  # Return the sessionmaker
    
    # Clean up after each test (drop tables)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop tables after each test
    await engine.dispose()
# Fixture for the test client, overriding database dependency
@pytest.fixture(scope="function")
def client(test_db):
    # Override the get_db dependency to use the in-memory database for each test
    app.dependency_overrides[get_db] = lambda: test_db()

    with TestClient(app) as client:
        yield client  # Return the TestClient instance
    
    client.close()