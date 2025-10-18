from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from .users import get_current_user_uuid
from ..schemas.withdrawal import WithdrawalCreate
from ..services.account_service import get_account_by_iban
from ..services.withdrawal_service import make_withdrawal

router = APIRouter(prefix="/withdrawals", tags=["withdrawals"])

@router.post("/{iban}")
def withdraw_money(iban: str, body: WithdrawalCreate, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    acc = get_account_by_iban(session, iban)
    if not acc or acc.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        wd = make_withdrawal(session, iban=iban, amount=body.amount)
        return {"iban": wd.account_iban, "amount": str(wd.amount), "date": wd.created_at}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
