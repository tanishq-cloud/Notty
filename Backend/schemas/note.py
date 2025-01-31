from pydantic import BaseModel
from datetime import datetime

class NoteCreateDTO(BaseModel):
    title: str
    body: str

class NoteUpdateDTO(BaseModel):
    title: str
    body: str
    note_id: int

class NoteResponseDTO(BaseModel):
    note_id: int
    title: str
    body: str
    modified_at: datetime
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True  


