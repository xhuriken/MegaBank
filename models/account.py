from ..utils import *
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel


class State(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    iban: str = Field(unique=True)
    balance: int = 0
    is_primary: bool = False
    state: State = State.ACTIVE
    user_id: int | None  = Field(default=None, foreign_key="user.id")
    
    def __init__(self, balance, is_primary, state, user_id):
            self.iban = create_iban(get_user(user_id).nationality)
            self.balance = balance
            self.is_primary = is_primary
            self.state = state
            self.user_id = user_id

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        self.balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        if self.balance < amount:
            raise ValueError("Not enough funds")
        self.balance -= amount

    def transit(self, amount: int, receiver: str):
        if self.iban == receiver:
            raise HTTPException(400, "Sender and receiver must differ")
    
        s: Account = self.iban
        r: Account = get_acc(receiver)

        s.withdraw(amount)
        r.deposit(amount)

        #TODO: save transition.
        #TODO: fonction pour return 1 transaction précise
        #TODO: function pour return toute les transaction d'un compte. (via iban dcp)
        #TODO: bien differentier dépot, transaction, withdraw (Ne pas afficher withdraw dans les fonction toto a faire)
        #TODO: Et ne pas record les transaction de withdraw et depost si elles sont utiliser pour une transition d'argent (ça ferai doublon)

    
        return {
        "sender":   {"iban": s.iban, "balance": s.balance},
        "receiver": {"iban": r.iban, "balance": r.balance},
        }

#TODO: pouvoir annuler les transaction !!!!!!!!!!!!!!!!


    #TODO: faire la route pour close un account d'un user !!
    def close(self):
        if self.state != State.CLOSED:
            self.state = State.CLOSED
