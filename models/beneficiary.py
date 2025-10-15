from typing import Optional
from sqlmodel import Field, SQLModel


class Beneficiary():
    name: str
    iban: str
    userid: int

    def __init__(self, name: str, iban: str, userid: int):
        self.name = name
        self.iban = iban
        self.userid = userid


class BeneficiaryDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    iban: str
    userid: Optional[int]