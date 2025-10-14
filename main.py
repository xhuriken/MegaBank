from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import TypedDict
from random import*

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

class TransactionHistory():
    date: str
    amount: int
    senderIban: str
    receiverIban: str

    def __init__(self,date,amount, senderIban, receiverIban):
        self.date = date
        self.amount = amount
        self.senderIban = senderIban
        self.receiverIban = receiverIban
    
    def __str__(self):
        return {self.date,self,self.amount,self.senderIban,self.receiverIban}

type Nationalities = {"FR","EN"}


Transactions = []

@app.get("/create_iban")
def create_iban(nat: str):
    iban: str
    control_key = 00
    megabank = 69420
    tab = []
    for i in range(100):    
        iban.append(randrange(0,9,1))
    rand: str = str(tab[0:5])
    rand2: str = str(tab[5:10])
    rand3: str = str(tab[11:22])
    iban: str = "nat" , control_key , " " , megabank , " " , rand , " " , rand2 , " " , rand3
    return iban




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

@app.get("/get_transactions")
def get_transactions():
    global Transactions
    return Transactions



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
    TH = TransactionHistory("Todey",amount,sender,receiver)
    Transactions.append(TH)
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
            return {"IBAN : " : iban, "Balance " : a.balance}
    return {"Iban no exista"}