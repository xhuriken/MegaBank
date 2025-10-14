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

class Account():
    iban: str
    balance: float
    userId: int

    def __init__(self, iban, balance, userId):
        self.iban = iban
        self.balance = balance
        self.userId = userId

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount need to be > 0")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount need to be > 0")
        if self.balance < amount:
            raise ValueError("Not enought bonk")
        self.balance -= amount
        

def get_acc(iban: str) -> Account:
    acc = accounts.get(iban)
    if not acc:
        raise HTTPException(404, "Iban not found")
    return acc



#MOVE in Utils class why not ?
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


#TODO adapt this for new archi
@app.post("/transit")
def transit(amount: float, sender: Account, receiver: Account):
    withdraw(amount, sender)
    deposit(amount, receiver)
    TH = TransactionHistory("Todey",amount,sender,receiver)
    Transactions.append(TH)
    return {"Receiver": receiver.balance, "Sender" : sender.balance}

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



users = {
    1 : User(1, "Jean", "1", "email","gyuezgef"),
    2 : User(2, "Fabrice", "2", "email","giugyyig"),
    3 : User(3, "test", "test", "email","huihuh"),
}

accounts = {
    "FR 0" : Account("FR 0", 10, "email"),
    "FR 1" : Account("FR 1", 100, "email"),
    "FR 2" : Account("FR 2", 30, "email"),
}

Transactions = []

class UserBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
class UserLogin(BaseModel):
    email: str
    password: str

typeUserActual = None

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