from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

#TODO make a type "nat" with only FR EN etc...
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nationality: str
    firstName: str
    lastName: str
    email: str = Field(unique=True, index=True)
    password: str

    def __init__(self, nationality, firstName, lastName, email, password):
            self.nationality = nationality
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.password = password

    #Function associate to user here

