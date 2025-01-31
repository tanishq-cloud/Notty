from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from fastapi import HTTPException, status

from models.model import User

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
