from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session  
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
DATABASE_URL = "sqlite+aiosqlite:///./Notes.db"
 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
 
def create_table():
    Base.metadata.create_all(bind=engine)
 
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()
 