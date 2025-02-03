from pydantic import BaseModel

class RefreshTokenDTO(BaseModel):
    refresh_token: str
    
class UserCreateDTO(BaseModel):
    username:str
    full_name:str
    password:str

    class Config:
        orm_mode=True
