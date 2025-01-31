from pydantic import BaseModel

class UserCreateDTO(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode=True
