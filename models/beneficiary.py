from typing import Optional
from sqlmodel import Field, SQLModel

class Beneficiary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    iban: str
    userid: int | None

    def __init__(self, name: str, iban: str, userid: int):
        self.name = name
        self.iban = iban
        self.userid = userid