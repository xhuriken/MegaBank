from pydantic import BaseModel

class UserBody(BaseModel):
    nationality: str
    first_name: str
    last_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str