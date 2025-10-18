from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from decimal import Decimal
from ..db.database import get_session
from ..core.auth import get_current_user_uuid
from ..schemas.account import AccountCreate, AccountPublic
from ..services.account_service import open_account, list_user_accounts, get_account_by_iban

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("", response_model=AccountPublic, status_code=201)
def create_account(body: AccountCreate, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    acc = open_account(session, user_uuid=user_uuid, is_primary=body.is_primary)
    return AccountPublic(iban=acc.iban, user_uuid=acc.user_uuid, balance=acc.balance, is_primary=acc.is_primary, state=acc.state.value)

@router.get("", response_model=list[AccountPublic])
def my_accounts(session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    accs = list_user_accounts(session, user_uuid)
    return [AccountPublic(iban=a.iban, user_uuid=a.user_uuid, balance=a.balance, is_primary=a.is_primary, state=a.state.value) for a in accs]

@router.get("/{iban}", response_model=AccountPublic)
def get_account(iban: str, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    acc = get_account_by_iban(session, iban)
    if not acc or acc.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountPublic(iban=acc.iban, user_uuid=acc.user_uuid, balance=acc.balance, is_primary=acc.is_primary, state=acc.state.value)
