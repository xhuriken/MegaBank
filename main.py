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
    password: str

    def __init__(self, id, firstName, lastName, email,password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

class Account():
    iban: str
    balance: float
    userId: int

    def __init__(self, iban, balance, userId):
        self.iban = iban
        self.balance = balance
        self.userId = userId

users = {
    1 : User(1, "Jean", "1", "email","gyuezgef"),
    2 : User(2, "Fabrice", "2", "email","giugyyig"),
    3 : User(3, "test", "test", "email","huihuh"),
}

accounts = {
    1 : Account("FR 0", 10, "email"),
    2 : Account("FR 1", 100, "email"),
    3 : Account("FR 2", 30, "email"),
}

class UserBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

@app.post("/register")
def register_user(user_data: UserBody):
    new_id = max(users.keys()) + 1

    for u in users.values():
        if u.email == user_data.email:
            raise HTTPException(status_code=400, detail="Sa existe deja nullos")

    new_user = User(
    id=new_id,
    firstName=user_data.first_name,
    lastName=user_data.last_name,
    email=user_data.email,
    password=user_data.password 
    )

    users[new_id] = new_user
    return {
    "message": "Tu existe maintenant",
    "first_name": new_user.firstName,
    "last_name": new_user.lastName
}

class UserLogin(BaseModel):
    email: str
    password: str

typeUserActual = None

@app.post("/login")
def login_user(credentials: UserLogin):
    global userAcutal

    for u in users.values():
        if u.email == credentials.email and u.password == credentials.password:
            typeUserActual = u  
           
            return {
                "message": f"Bienvenue {u.firstName}, t’es vraiment le GOAT !",
                "user": typeUserActual
            }

    raise HTTPException(status_code=401, detail="Identifiants invalides")

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