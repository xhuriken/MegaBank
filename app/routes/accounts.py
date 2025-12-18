from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from decimal import Decimal
from ..db.database import get_session
from ..core.auth import get_current_user_uuid
from ..schemas.account import AccountCreate, AccountPublic
from ..services.account_service import open_account, list_user_accounts, get_account_by_iban, close_account

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("", response_model=AccountPublic, status_code=201)
def create_account(
    body: AccountCreate, 
    session: Session = Depends(get_session), 
    user_uuid: str = Depends(get_current_user_uuid)):
    try:
        acc = open_account(
            session,
            user_uuid=user_uuid,
            is_primary=body.is_primary,
            account_name=body.name
        )
        return AccountPublic(
            iban=acc.iban,
            user_uuid=acc.user_uuid,
            balance=acc.balance,
            is_primary=acc.is_primary,
            state=acc.state.value,
            name=acc.name
        )
    except ValueError as e:
        #  "Account limit reached (5)" or "User already has a primary account"
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[AccountPublic])
def my_accounts(session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    accs = list_user_accounts(session, user_uuid)
    return [AccountPublic(iban=a.iban, user_uuid=a.user_uuid, balance=a.balance, is_primary=a.is_primary, state=a.state.value, name=a.name) for a in accs]

@router.get("/{iban}", response_model=AccountPublic)
def get_account(iban: str, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    acc = get_account_by_iban(session, iban)
    if not acc or acc.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountPublic(iban=acc.iban, user_uuid=acc.user_uuid, balance=acc.balance, is_primary=acc.is_primary, state=acc.state.value, name=acc.name)

@router.delete("/{iban}", response_model=AccountPublic)
def close_user_account(
    iban: str,
    session: Session = Depends(get_session),
    user_uuid: str = Depends(get_current_user_uuid),
):
    acc = get_account_by_iban(session, iban)
    if not acc or acc.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Account not found")

    if acc.is_primary:
        raise HTTPException(status_code=400, detail="Primary account cannot be closed")

    # trouver compte principal de l'user
    primary = next(
        (a for a in list_user_accounts(session, user_uuid) if a.is_primary),
        None
    )
    if not primary:
        raise HTTPException(status_code=400, detail="Primary account not found")

    try:
        closed = close_account(session, iban=iban, fallback_iban=primary.iban)
        return AccountPublic(
            iban=closed.iban,
            user_uuid=closed.user_uuid,
            balance=closed.balance,
            is_primary=closed.is_primary,
            state=closed.state.value,
            name=closed.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
