from typing import Optional
from sqlmodel import Field, SQLModel

class Beneficiary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    iban: str = Field(index=True, unique=False) 
    
    userid: int = Field(foreign_key="user.id", index=True)