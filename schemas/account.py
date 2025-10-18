from pydantic import BaseModel
from decimal import Decimal

class AccountCreate(BaseModel):
    # option: is_primary, sinon False par défaut
    is_primary: bool = False

class AccountPublic(BaseModel):
    iban: str
    user_uuid: str
    balance: Decimal
    is_primary: bool
    state: str
