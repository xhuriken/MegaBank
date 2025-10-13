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
<<<<<<< HEAD
    return {"message": "Bienvenue sur FastAPI!"}
=======
    return {"message": "Bienvenue sur FastAPI!"}


class Account(BaseModel):
    name: str
    balance: float

account = Account(name="Fabrice", balance=100)
account2 = Account(name="Eboue", balance=5)

@app.get("/get_balance")
def get_balance(acc: Account):
    return {"solde": acc.balance}

@app.post("/deposit")
def deposit(amount: float, acc: Account):
    acc.balance += amount
    return {"solde": acc.balance}

@app.post("/withdraw")
def withdraw(amount: float, acc: Account):
    if(acc.balance < amount):
        raise HTTPException(status_code=400, detail="T'a pas la thune")
    else:
        acc.balance -= amount
    return {"solde": acc.balance}

@app.post("/transit")
def transit(amount: float, sender: Account, receiver: Account):
    withdraw(amount, sender)
    deposit(amount, receiver)
    return {"Receiver": receiver.balance, "Sender" : sender.balance}

@app.get("/me")
def account_info(acc: Account):
    return {"Name: " : acc.name, "Balance" : acc.balance}


#this working heoryaeporuhaer
transit(5, account, account2)
#python ça pu wallah
print(account_info(account) , " | " , account_info(account2))
>>>>>>> main
