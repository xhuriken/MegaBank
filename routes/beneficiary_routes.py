from fastapi import APIRouter, HTTPException
from ..models.beneficiary import Beneficiary
from ..state import *

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])


@router.get("/create")
def create_beneficiary(userid: int, name: str, iban: str):
    if userid not in users:
        raise HTTPException(status_code=404, detail=f"Utilisateur ID {userid} n'existe pas.")

    iban_exists = any(a.iban == iban for a in accounts.values())
    if not iban_exists:
        raise HTTPException(status_code=400, detail=f"IBAN {iban} du bénéficiaire n'est pas un compte connu.")

    new_id = max(beneficiaries.keys()) + 1

    new_beneficiary = Beneficiary(name=name, iban=iban, userid=userid)

    beneficiaries[new_id] = new_beneficiary

    return {
        "message": f"Bénéficiaire '{name}' (IBAN: {iban}) ajouté pour l'utilisateur ID {userid}.",
    }