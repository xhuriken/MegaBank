from typing import Optional
from pydantic import BaseModel

class BeneficiaryCreate(BaseModel):
    name: Optional[str] = None
    iban: str