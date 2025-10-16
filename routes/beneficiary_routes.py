from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from ..models.beneficiary import Beneficiary
from ..models.user import User
from ..models.account import Account
from ..schemas.beneficiary_schema import BeneficiaryCreate
from ..database import engine
from ..security.verify_token import get_current_user


router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_beneficiary(payload: BeneficiaryCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:

        account = session.exec(select(Account).where(Account.iban == payload.iban)).first()
        if not account:
            raise HTTPException(status_code=400, detail="iban doesn't exist")

        owner = session.get(User, account.user_id) if getattr(account, "user_id", None) else None

        if owner and getattr(owner, "id", None) == getattr(current_user, "id", None):
            raise HTTPException(status_code=400, detail="you canot add your acount as a beneficiary")

        name = (payload.name or "").strip()
        if not name:
            if owner:
                name = f"{owner.firstName} {owner.lastName}".strip()
            else:
                raise HTTPException(status_code=400, detail="name must not be empty")

        new_beneficiary = Beneficiary(name=name, iban=payload.iban, userid=current_user.id)
        session.add(new_beneficiary)
        session.commit()
        session.refresh(new_beneficiary)

        return {
            "message": f"Bénéficiaire '{name}' (IBAN: {payload.iban}) ajouté pour l'utilisateur ID {current_user.id}.",
            "id": new_beneficiary.id,
        }

@router.get("/", status_code=status.HTTP_200_OK)
def list_beneficiaries(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        beneficiaries = session.exec(
            select(Beneficiary).where(Beneficiary.userid == current_user.id)
        ).all()

        return [
            {"id": b.id, "name": b.name, "iban": b.iban}
            for b in beneficiaries
        ]