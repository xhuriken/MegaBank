from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    uuid: str
    email: EmailStr
    first_name: str
    last_name: str
