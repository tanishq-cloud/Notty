# import pytest
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from database import Base 
# from sqlalchemy.orm import sessionmaker
# from fastapi.testclient import TestClient

# TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# TestSessionLocal = async_sessionmaker(
#     bind=test_engine, class_=AsyncSession, expire_on_commit=False
# )

# @pytest_asyncio.fixture(scope="function")
# async def override_get_db():
#     """Provides a fresh test database session per test"""
#     async with TestSessionLocal() as session:
#         yield session
#         await session.rollback() 

# @pytest.fixture(scope="function")
# async def override_get_db():
#     # In-memory SQLite for tests
#     SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
#     engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
#     TestingSessionLocal = sessionmaker(
#         engine, class_=AsyncSession, expire_on_commit=False
#     )

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all) 
    
#     yield TestingSessionLocal 
    
  
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)  

# # @pytest_asyncio.fixture(scope="function", autouse=True)
# # async def setup_db():
# #     """Setup and teardown the test database"""
# #     test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
# #     async with test_engine.begin() as conn:
# #         await conn.run_sync(Base.metadata.create_all)
# #     yield
# #     async with test_engine.begin() as conn:
# #         await conn.run_sync(Base.metadata.drop_all) 

# @pytest.fixture
# def setup_db(test_db):
#     # Override the get_db dependency to use the in-memory database for each test
#     app.dependency_overrides[get_db] = lambda: test_db()

#     with TestClient(app) as client:
#         yield client  # Return the TestClient instance

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import Base, get_db  # Assuming this contains your SQLAlchemy models
from main import app  # Import your FastAPI app instance

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def override_get_db():
    """Provides a fresh test database session per test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    TestingSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Yield a session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def setup_db(override_get_db):
    """Override the get_db dependency to use the in-memory database for each test."""
    app.dependency_overrides[get_db] = lambda: override_get_db
    with TestClient(app) as client:
        yield client  # Return the TestClient instance