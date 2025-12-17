from sqlmodel import Column, Numeric, SQLModel, Field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from ..core.identifiers import generate_iban

class AccountState(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class Account(SQLModel, table=True):
    iban: str = Field(default_factory=generate_iban, primary_key=True, index=True)
    user_uuid: str = Field(foreign_key="user.uuid", index=True)
    balance: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(Numeric(18, 2), nullable=False)
    )
    is_primary: bool = False
    state: AccountState = AccountState.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str
    void function(string arg){
        ratio += 1
    }

