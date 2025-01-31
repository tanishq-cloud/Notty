import os
from fastapi.responses import StreamingResponse
import pandas as pd
from fastapi import  Depends, HTTPException, BackgroundTasks,APIRouter,Response
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sendgrid.helpers.mail import Mail
import ssl
from dotenv import  load_dotenv
from sqlalchemy.orm import Session

from schemas.note import NoteCreateDTO,NoteResponseDTO
from dao.note_dao import NoteDAO
from db.database import get_db
load_dotenv()

ssl._create_default_https_context=ssl._create_unverified_context

router = APIRouter()


@router.post("/addnote", response_model=NoteResponseDTO)
async def create_task(note: NoteCreateDTO,db:Session=Depends(get_db)):
    note_dao=NoteDAO(db)
    # note_dict=
    
    print(note.model_dump())
    return note_dao.create_note(**note.model_dump())
