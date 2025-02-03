from pydantic import BaseModel

class UserCreateDTO(BaseModel):
    username:str
    full_name:str
    password:str

    class Config:
        orm_mode=True
