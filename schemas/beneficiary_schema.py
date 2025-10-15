from pydantic import BaseModel

class BeneficiaryCreate(BaseModel):
    userid: int
    name: str
    iban: str