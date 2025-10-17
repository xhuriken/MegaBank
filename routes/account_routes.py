from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import date

# from models import account
from ..security.verify_token import get_current_user
from ..models.user import User
from ..models.account import Account, State
from ..database import engine
from ..utils import create_iban

router = APIRouter(prefix="/accounts", tags=["Accounts"])

today = date.today()
special_day = date(2025, 12, 25)


def get_account(session: Session, iban: str) -> Account:
    account = session.exec(select(Account).where(Account.iban == iban)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/open")
def open_account(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        user = session.get(User, current_user.id)
        if not user:
            raise HTTPException(status_code=400, detail="User doesn't exist")

        nb_accounts = session.exec(
            select(Account).where(Account.user_id == user.id)
        ).all()

        if len(nb_accounts) >= 5:
            raise HTTPException(status_code=400, detail="You can't have more than 5 accounts")

        balance = 200 if today == special_day else 100 if len(nb_accounts) == 0 else 0
        is_primary = len(nb_accounts) == 0

        

        new_account = Account(

            balance=balance,
            is_primary=is_primary,
            state=State.ACTIVE,
            user_id=user.id
        )

        session.add(new_account)
        session.commit()
        session.refresh(new_account)

        return {
            "message": "Account created successfully!",
            "iban": new_account.iban,
            "balance": new_account.balance,
            "state": new_account.state
        }


@router.get("/balance/{iban}")
def get_balance(iban: str, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        account = get_account(session, iban)
        if account.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized access")
        return {"iban": account.iban, "balance": account.balance}


@router.post("/deposit/{iban}")
def deposit(iban: str, amount: float, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        account = get_account(session, iban)
        if account.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized access")

        try:
            account.deposit(amount)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        session.add(account)
        session.commit()
        session.refresh(account)
        return {"iban": account.iban, "balance": account.balance}


@router.post("/withdraw/{iban}")
def withdraw(iban: str, amount: float, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        account = get_account(session, iban)
        if account.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized access")

        try:
            account.withdraw(amount)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        session.add(account)
        session.commit()
        session.refresh(account)
        return {"iban": account.iban, "balance": account.balance}

@router.delete("/del/{iban}")
def del_account(iban: str, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        account = get_account(session, iban)

        if account.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized access")
        if account.is_primary:
            raise HTTPException(status_code=400, detail="Primary account can't be closed")
        if account.state == State.CLOSED:
            raise HTTPException(status_code=400, detail="Account already closed")

        account.close()
        session.add(account)
        session.commit()
        session.refresh(account)

        return {
            "message": f"Account {account.iban} closed successfully.",
            "iban": account.iban,
            "state": account.state
        }

@router.get("/my_accounts")
def get_user_accounts(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        accounts = (
            session.query(Account)
            .filter(Account.user_id == current_user.id)
            .all()
        )

        result = [
            {
                "iban": acc.iban,
                "balance": acc.balance,
                "state": acc.state,
                "is_primary": acc.is_primary
            }
            for acc in accounts
        ]

        return {"user_id": current_user.id, "accounts": result}
