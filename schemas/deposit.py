from decimal import Decimal
from pydantic import BaseModel, Field

class DepositCreate(BaseModel):
    amount: Decimal = Field(gt=Decimal("0"), max_digits=18, decimal_places=2)