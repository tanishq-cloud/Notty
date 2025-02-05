from sqlalchemy import ForeignKey, String, Text, DateTime, func,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime

from ..db.database import Base

class User(Base):
    __tablename__ = "users"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    notes: Mapped[List["Note"]] = relationship(back_populates="user")
 
class Note(Base):
    __tablename__ = "notes"
 
    note_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    modified_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
 
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
 
    user: Mapped["User"] = relationship(back_populates="notes")