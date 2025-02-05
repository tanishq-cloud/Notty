from sqlalchemy import select
from sqlalchemy.orm import Session

from models.model import Note
 
class NoteDAO:
    def __init__(self, db: Session):
        self.db = db
 
    async def create_note(self, title: str, body: str, user_id: int):
        note = Note(title=title, body=body, user_id=user_id)
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note
 
    async def get_note_by_id(self, note_id: int):

        result = await self.db.execute( select(Note).filter(Note.note_id == note_id))
        return result.scalars().first()
 
    async def get_notes_by_user(self, user_id: int):
        result = await self.db.execute( select(Note).filter(Note.user_id == user_id))
        return result.scalars().all()
 
    async def update_note(self, note_id: int, title: str, body: str):
        note = await self.get_note_by_id(note_id)
        if note:
            note.title = title
            note.body = body
            await self.db.commit()
            await self.db.refresh(note)
        return note
 
    async def delete_note(self, note_id: int):
        note = await self.get_note_by_id(note_id)
        if note:
            await self.db.delete(note)
            await self.db.commit()
        return note