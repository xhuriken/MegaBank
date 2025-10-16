from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from ..security.verify_token import get_current_user
from ..models.user import User
from ..utils import create_iban, get_acc
from ..database import engine
from ..models.account import Account, State

router = APIRouter(prefix="/accounts", tags=["Accounts"])

#TODO when user is created, call open_account with his id

@router.post("/open")
def open_account(current_user: User = Depends(get_current_user)):

    with Session(engine) as session:
        
        user = session.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User doesn't exist")

        balance = 0
        # nb_found_accounts = 0
        isPrimary = False

        accounts = session.query(Account).filter(Account.user_id == current_user.id)

        nb_found_accounts = accounts.count()

        if nb_found_accounts >= 5:
            return {"message": "You can't have more than 5 account"}

        if nb_found_accounts == 0:
            #TODO balance must be different with special date
            balance = 100
            isPrimary = True

        #TODO REACT select nationality
        iban = create_iban("FR");
        new_account = Account(iban, balance, isPrimary, State.ACTIVE, current_user.id)

        session.add(new_account)
        session.commit()
        session.refresh(new_account)  

        return {"message": "Compte créé", "iban": new_account.iban, "balance": new_account.balance}

@router.get("/balance/{iban}")
def get_balance(iban: str):
    acc = get_acc(iban)
    return {"iban": acc.iban, "balance": acc.balance}

@router.post("/deposit/{iban}")
def deposit(iban: str, amount: float):
    acc = get_acc(iban)
    try:
        #Deposit can make error "Value Error" go see in the Account class
        acc.deposit(amount)
    except ValueError as e:
        #If it this case, throw HTTPException and print the exeption
        raise HTTPException(400, str(e))
    return {"iban": acc.iban, "balance": acc.balance}


@router.post("/withdraw/{iban}")
def withdraw(iban: str, amount: float):
    acc = get_acc(iban)
    try:
        acc.withdraw(amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"iban": acc.iban, "balance": acc.balance}

@router.get("/")
def account_info(iban: str):
    acc = get_acc(iban)
    #TODO return account's user name ??
    # other infos too ?
    return {"iban": acc.iban, "balance": acc.balance}