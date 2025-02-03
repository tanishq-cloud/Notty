from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_session

import jwt
import os

from db import database
from dao.user_dao import UserDAO
from schemas.user import UserCreateDTO

router = APIRouter()


@router.post("/register/")
async def create_user(user_data: UserCreateDTO, db: async_session = Depends(database.get_db)):
    """Registers a new user"""
    try:
        user_dao = UserDAO(db)
        created_user = await user_dao.create_user(user_data.username, user_data.password)

        if created_user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        ) 
        # HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        return {"message": "User created successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}",
        ) from e

@router.post("/token/")
async def token(user: OAuth2PasswordRequestForm = Depends(), db: async_session = Depends(database.get_db)):
    """Generates a JWT token for authentication"""
    try:
        user_dao = UserDAO(db)
        user_retrieved =await  user_dao.authenticate_user(user.username, user.password)

        if user_retrieved is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        access_token = user_dao.create_access_token({"sub": user_retrieved.username})

        return {"access_token": access_token, "token_type": "bearer"}

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token generation failed") from e

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}") from e
