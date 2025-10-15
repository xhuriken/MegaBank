from fastapi import APIRouter, HTTPException
from ..utils import get_acc
from ..state import *
from ..models.account import Account

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/open")
def open_account(userId: int):

    #check if user exist
    if userId not in users:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")

    balance = 0
    nb_found_accounts = 0
    isPrimary = False

    for i in accounts.values():
        if i.userId == userId:
            nb_found_accounts += 1

    if nb_found_accounts >= 5:
        return {"message": "Arrête de créer des comptes t'en à déjà trop"}

    if nb_found_accounts == 0:
        balance = 100
        isPrimary = True

    new_id = len(accounts) + 1
    iban = f"FR {new_id}"
    new_account = Account(iban, balance, isPrimary, userId)
    accounts[iban] = new_account

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
    for a in accounts.values():
        if(a.iban == iban):
            return {"IBAN : " : iban, "Balance " : a.balance}
    return {"erreur": "Account not found"}