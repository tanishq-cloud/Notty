from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.model import  User
from dao.note_dao import NoteDAO
from schemas.note import NoteCreateDTO, NoteResponseDTO
from dao import user_dao
from db.database import get_db
from typing import List

router = APIRouter(prefix="/note")

# Create a note
@router.post("/", response_model=NoteResponseDTO)
async def create_note(note: NoteCreateDTO, current_user: User = Depends(user_dao.get_current_user), db: Session = Depends(get_db)):
    """Creates a new note linked to the current user"""
    try:
        note_dao = NoteDAO(db)
        new_note = note_dao.create_note(
            title=note.title,
            body=note.body,
            user_id=current_user.id
        )
        return new_note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating note")


@router.get("/all", response_model=List[NoteResponseDTO])
async def get_notes(current_user: User = Depends(user_dao.get_current_user), db: Session = Depends(get_db)):
    """Fetches all notes created by the current user"""
    try:
        note_dao = NoteDAO(db)
        notes = note_dao.get_notes_by_user(current_user.id)
        # if not notes:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found for the user")
        return notes
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving notes")




@router.get("/{note_id}", response_model=NoteResponseDTO)
async def get_note(note_id: int, current_user: User = Depends(user_dao.get_current_user), db: Session = Depends(get_db)):
    """Fetches a note by its ID"""
    try:
        note_dao = NoteDAO(db)
        note = note_dao.get_note_by_id(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this note")
        return note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving note")


@router.put("/{note_id}", response_model=NoteResponseDTO)
async def update_note(note_id: int, note: NoteCreateDTO, current_user: User = Depends(user_dao.get_current_user), db: Session = Depends(get_db)):
    """Updates a note's title or body"""
    try:
        note_dao = NoteDAO(db)
        existing_note = note_dao.get_note_by_id(note_id)
        if existing_note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if existing_note.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this note")
        
        updated_note = note_dao.update_note(
            note_id=note_id,
            title=note.title,
            body=note.body
        )
        return updated_note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating note")


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, current_user: User = Depends(user_dao.get_current_user), db: Session = Depends(get_db)):
    """Deletes a note by its ID"""
    try:
        note_dao = NoteDAO(db)
        note = note_dao.get_note_by_id(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this note")
        
        note_dao.delete_note(note_id)
        return {"message": "Note successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting note")
