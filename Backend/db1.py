# db.py (Database setup)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # In-memory SQLite for tests

# Create an async engine for the in-memory database
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Create a session factory
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get the session
async def get_db():
    async with TestingSessionLocal() as session:
        yield session
