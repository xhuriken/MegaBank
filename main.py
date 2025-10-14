from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import TypedDict
from sqlmodel import Field, SQLModel, Session, create_engine, select
from utils import *
from state import *
from models import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur FastAPI!"}


@app.post("/open_account")
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

    return {
        "message": "Compte créé avec succès",
        "id": new_id,
        "iban": new_account.iban,
        "balance": new_account.balance,
        "userId": new_account.userId
    }

@app.get("/balance/{iban}")
def get_balance(iban: str):
    acc = get_acc(iban)
    return {"iban": acc.iban, "balance": acc.balance}


@app.post("/deposit/{iban}")
def deposit(iban: str, amount: float):
    acc = get_acc(iban)
    try:
        #Deposit can make error "Value Error" go see in the Account class
        acc.deposit(amount)
    except ValueError as e:
        #If it this case, throw HTTPException and print the exeption
        raise HTTPException(400, str(e))
    return {"iban": acc.iban, "balance": acc.balance}


@app.post("/withdraw/{iban}")
def withdraw(iban: str, amount: float):
    acc = get_acc(iban)
    try:
        acc.withdraw(amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"iban": acc.iban, "balance": acc.balance}


@app.post("/transit")
def transit(amount: float, sender: str, receiver: str):
    if sender == receiver:
        raise HTTPException(400, "Sender and receiver must differ")
    
    s = get_acc(sender)
    r = get_acc(receiver)

    try:
        s.withdraw(amount)
        r.deposit(amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return {
        "sender":   {"iban": s.iban, "balance": s.balance},
        "receiver": {"iban": r.iban, "balance": r.balance},
    }


#GESTION USER

@app.get("/me")
def user_info(usrId: int):
    for i in users.values():
        if(i.id == usrId):
            return {"First Name: " : i.firstName, "Last Name" : i.lastName, "Email" : i.email}
    return {"user no exista"}    
    

@app.get("/account")
def account_info(iban: str):
    for a in accounts.values():
        if(a.iban == iban):
            return {"IBAN : " : iban, "Balance " : a.balance}
    return {"Iban no exista"}


@app.get("/create_beneficiary")
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


class UserBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
class UserLogin(BaseModel):
    email: str
    password: str



@app.post("/register")
def register_user(user_data: UserBody):
    new_id = max(users.keys()) + 1

    for u in users.values():
        if u.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already exist")

    new_user = User(
        id=new_id,
        firstName=user_data.first_name,
        lastName=user_data.last_name,
        email=user_data.email,
        password=user_data.password 
    )

    users[new_id] = new_user
    return {
        "message": "New account created !",
        "first_name": new_user.firstName,
        "last_name": new_user.lastName
    }

@app.post("/login")
def login_user(credentials: UserLogin):
    global userAcutal

    for u in users.values():
        if u.email == credentials.email and u.password == credentials.password:
            typeUserActual = u  
           
            return {
                "message": f"Bienvenue {u.firstName}, You're connected",
                "user": typeUserActual
            }

    raise HTTPException(status_code=401, detail="Bad credentials")