
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.model import User
import jwt
from datetime import datetime, timedelta
import os
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, password: str):
        hashed_password = pwd_context.hash(password)
        user = User(username=username, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if user and pwd_context.verify(password, user.password):
            return user
        return None
    
    def create_access_token(self,data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)