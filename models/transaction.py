from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import datetime
from core.identifiers import new_uuid

class Transaction(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)
    source_iban: str = Field(foreign_key="account.iban", index=True)
    target_iban: str = Field(foreign_key="account.iban", index=True)
    amount: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    label: str | None = None