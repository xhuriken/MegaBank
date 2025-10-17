from random import randrange
from fastapi import FastAPI, Depends, HTTPException


from sqlmodel import Session, select
from .database import engine

def get_acc(iban: str):
    with Session(engine) as session:
        from .models.account import Account
        statement = select(Account).where(Account.iban == iban)
        acc = session.exec(statement).first()

        if not acc:
            raise HTTPException(status_code=404, detail="IBAN not found")

        return acc

def get_user(user_id: int):
    with Session(engine) as session:
        from .models.user import User
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(status_code=404, detail="user not found")
    return user

def create_iban(nat: str):
    iban: str
    control_key = "00"
    megabank = "69420"
    rand: str = random_numbers(5)
    rand2: str = random_numbers(5)
    rand3: str = random_numbers(11)
    iban: str = nat + control_key + " " + megabank + " " + rand + " " + rand2 + " " + rand3
    return iban

def random_numbers(amount: int):
    rep = ""
    for i in range(amount):
        rep += str(randrange(0,9,1))
    return rep