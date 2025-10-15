from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User():
    id: int
    firstName: str
    lastName: str
    email: str
    password: str

    def __init__(self, id, firstName, lastName, email,password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

class UserDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstName: str
    lastName: str
    email: str = Field(unique=True, index=True)
    password: str

    # accounts: List["AccountBDD"] = Relationship(back_populates="user")
