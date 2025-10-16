from ..tresitil import*
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

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        if self.balance < amount:
            raise ValueError("Not enough funds")
        self.balance -= amount


    #TODO: faire la route pour close un account d'un user !!
    def close(self):
        if self.state != State.CLOSED:
            self.state = State.CLOSED
