from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.database import get_session
from core.auth import get_current_user_uuid
from schemas.deposit import DepositCreate
from services.account_service import get_account_by_iban
from services.deposit_service import make_deposit

router = APIRouter(prefix="/deposits", tags=["deposits"])

@router.post("/{iban}")
def deposit_money(iban: str, body: DepositCreate, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    acc = get_account_by_iban(session, iban)
    if not acc or acc.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        dep = make_deposit(session, iban=iban, amount=body.amount)
        return {"iban": dep.account_iban, "amount": str(dep.amount), "date": dep.created_at}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
