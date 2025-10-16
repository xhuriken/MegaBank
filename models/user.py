from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    firstName: str
    lastName: str
    email: str = Field(unique=True, index=True)
    password: str

    def __init__(self, firstName, lastName, email, password):
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.password = password

    #Function associate to user here

