from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import TypedDict
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur FastAPI!"}

class User():
    id: int
    firstName: str
    lastName: str
    email: str

    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

class Account():
    iban: str
    balance: float
    isPrimary: bool
    userId: int

    def __init__(self, iban, balance, isPrimary, userId):
        # c'est pour la bdd ça self.id = id
        self.iban = iban
        self.balance = balance
        self.isPrimary = isPrimary
        self.userId = userId

users = {
    1 : User(1, "Jean", "1", "email"),
    2 : User(2, "Fabrice", "2", "email"),
    3 : User(3, "test", "test", "email"),
}

accounts = {
    1 : Account("FR 0", 10, True, 1),
    2 : Account("FR 1", 100, True, 2),
    3 : Account("FR 2", 30, False, 1),
    4 : Account("FR 3", 30, False, 1),
    5 : Account("FR 4", 30, False, 1),
    6 : Account("FR 5", 30, False, 1),
}
@app.post("/open_account")
def open_account(userId: int):

    #check if user exist
    if userId not in users:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")

    balance = 0
    nb_found_accounts = 0
    isPrimary = False

    for bite in accounts.values():
        if bite.userId == userId:
            nb_found_accounts += 1

    if nb_found_accounts >= 5:
        return {"message": "Arrête de créer des comptes t'en à déjà trop"}

    if nb_found_accounts == 0:
        balance = 100
        isPrimary = True

    new_id = max(accounts.keys()) + 1
    iban = f"FR {new_id}"
    new_account = Account(iban, balance, isPrimary, userId)
    accounts[new_id] = new_account

    return {
        "message": "Compte créé avec succès",
        "id": new_id,
        "iban": new_account.iban,
        "balance": new_account.balance,
        "userId": new_account.userId
    }



@app.get("/get_balance")
def get_balance(iban: str):
    for a in accounts.values():
        if(a.iban == iban):
            return {"solde":a.balance, "Iban" : iban}
    return "Iban ne exista"


@app.post("/deposit")
def deposit(amount: float, iban: str):
    for a in accounts.values():
        if(a.iban == iban):
            a.balance += amount
            return {"solde": a.balance}
    return {"Iban no exista"}


@app.post("/withdraw")
def withdraw(amount: float, iban: str):
    for a in accounts.values():
        if(a.iban == iban):
            if(a.balance < amount):
                raise HTTPException(status_code=400, detail="T'a pas la thune")
            else:
                a.balance -= amount
            return {"solde": a.balance}
    return {"Iban no exista"}


@app.post("/transit")
def transit(amount: float, sender: str, receiver: str):
    withdraw(amount, sender)
    deposit(amount, receiver)
    return {"Receiver": get_balance(receiver), "Sender" : get_balance(sender)}

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
            return {"IBAN : " : iban, "Balance " : a.balance, "isPrimary " : a.isPrimary, "userId" : a.userId}
    return {"Iban no exista"}