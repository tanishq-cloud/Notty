from fastapi import Form
from pydantic import BaseModel

class RefreshTokenDTO(BaseModel):
    refresh_token: str
    
class UserCreateDTO(BaseModel):
    username:str
    full_name:str
    password:str

    class Config:
        orm_mode=True

# class UserCreateDTO(BaseModel):
#     username: str = Form(..., min_length=3)  # username is required and must be at least 3 characters
#     password: str = Form(..., min_length=6)  # password is required and must be at least 6 characters
#     full_name: str = Form(...)  # full_name is required
#     class Config:
#         orm_mode=True