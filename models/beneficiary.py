from sqlmodel import SQLModel, Field
from datetime import datetime
from core.identifiers import new_uuid


class Beneficiary(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True, index=True)
    user_uuid: str = Field(foreign_key="user.uuid", index=True)

    name: str
    iban: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
