from pydantic import BaseModel


class BeneficiaryCreate(BaseModel):
    name: str
    iban: str


class BeneficiaryPublic(BaseModel):
    id: str
    user_uuid: str
    name: str
    iban: str
