from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import TypedDict
from sqlmodel import Field, SQLModel, Session, create_engine, select

#pydantic gestion de model

#GESTION DERREUR: raise HTTPException(status_code=400, detail="ERREUR")

#Liste
mon_tab = [5, 8, 6, 9]
m = [[1, 3, 4],
     [5, 6, 8],
     [2, 1, 3],
     [7, 8, 15]]

#Dictionaire
tableau = {
    1: 50.0,
    2: 3.0
}
#Dictionaire
tableau2con2 = {
    1: {"name": "Fabrice",      "id": 1},
    2: {"name": "Emile louis",  "id": 2},
    3: {"name": "éboué",        "id": 3},
}



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
    userId: int

    def __init__(self, iban, balance, userId):
        # c'est pour la bdd ça self.id = id
        self.iban = iban
        self.balance = balance
        self.userId = userId

users = {
    1 : User(1, "Jean", "1", "email"),
    2 : User(2, "Fabrice", "2", "email"),
    3 : User(3, "test", "test", "email"),
}

accounts = {
    1 : Account("FR 0", 10, "email"),
    2 : Account("FR 1", 100, "email"),
    3 : Account("FR 2", 30, "email"),
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
            #Erreur avec le return (500) si je met return {"a"} pas d'erreur
            # problème avec le users[usrId] ?
            return {"First Name: " : i.firstName, "Last Name" : i.lastName, "Email" : i.email}
    return {"user no exista"}    
    

@app.get("/account")
def account_info(iban: str):
    for a in accounts.values():
        if(a.iban == iban):
            return {"IBAN : " : iban, "Balance " : a.balance}
    return {"Iban no exista"}

#this working heoryaeporuhaer
# transit(5, account, account2)
# print(account_info(account) , " \n " , account_info(account2))
# print(user_info(userActual))
