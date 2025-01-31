from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status

from models.model import User
from db import database

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class UserDAO:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, username: str, password: str):
        """Creates a new user in the database"""
        try:
            hashed_password = self.pwd_context.hash(password)
            user = User(username=username, hashed_password=hashed_password)
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return user

        except IntegrityError:
            self.db.rollback()
            return None  # Returning None to handle duplicate username errors

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

    def get_user_by_username(self, username: str):
        """Retrieves a user by username"""
        try:
            return self.db.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

    def authenticate_user(self, username: str, password: str):
        """Authenticates a user by verifying password"""
        try:
            user = self.get_user_by_username(username)
            if user and self.pwd_context.verify(password, user.hashed_password):
                return user
            return None
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        """Generates a JWT access token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"exp": expire})
            return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Token generation error: {str(e)}")
    def decode_access_token(self, token: str):
        """Decodes and validates the JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> User:
    """Dependency that fetches the current user based on the provided token."""
    user_dao = UserDAO(db)
    
    payload = user_dao.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    db_user = user_dao.get_user_by_username(payload.get("sub"))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user
