from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel



class Account():
    iban: str
    balance: float
    isPrimay: bool
    userId: int

    def __init__(self, iban, balance, isPrimay, userId):
        self.iban = iban
        self.balance = balance
        self.isPrimay = isPrimay
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

class AccountBDD(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    iban: str = Field(index=True, unique=True)
    balance: float = 0
    isPrimary: bool = False

    user_id: Optional[int] = Field(default=None, foreign_key="userbdd.id")

    # user: Optional["UserBDD"] = Relationship(back_populates="accounts")
    # sent_transactions: List["TransactionHistoryBDD"] = Relationship(back_populates="sender_account", sa_relationship_kwargs={"foreign_keys": "[TransactionHistoryBDD.sender_id]"})
    # received_transactions: List["TransactionHistoryBDD"] = Relationship(back_populates="receiver_account", sa_relationship_kwargs={"foreign_keys": "[TransactionHistoryBDD.receiver_id]"})

