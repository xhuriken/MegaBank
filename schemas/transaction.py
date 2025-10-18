from decimal import Decimal
from pydantic import BaseModel, Field

class TransferCreate(BaseModel):
    source_iban: str
    target_iban: str
    amount: Decimal = Field(gt=Decimal("0"), max_digits=18, decimal_places=2)