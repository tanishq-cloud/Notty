from sqlalchemy.orm import Session

from models.model import Note

 
class NoteDAO:
    def __init__(self, db: Session):
        self.db = db
 
    def create_note(self, title: str, body: str, user_id: int):
        note = Note(title=title, body=body, user_id=user_id)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
 
    def get_note_by_id(self, note_id: int):
        return self.db.query(Note).filter(Note.note_id == note_id).first()
 
    def get_notes_by_user(self, user_id: int):
        return self.db.query(Note).filter(Note.user_id == user_id).all()
 
    def update_note(self, note_id: int, title: str, body: str):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = title
            note.body = body
            self.db.commit()
            self.db.refresh(note)
        return note
 
    def delete_note(self, note_id: int):
        note = self.get_note_by_id(note_id)
        if note:
            self.db.delete(note)
            self.db.commit()
        return note