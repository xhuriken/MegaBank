from typing import List, Optional
from sqlmodel import Enum, Field, Relationship, SQLModel
from enum import Enum

#TODO: Rename this class ? "transaction" ?

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType
    amount: int
    note: Optional[str] = None

    sender_id: Optional[int] = Field(default=None, foreign_key="account.id")
    receiver_id: Optional[int] = Field(default=None, foreign_key="account.id")

    def __init__(self,type,date,amount, note, sender_id, receiver_id):
        self.type = type
        self.date = date
        self.amount = amount
        self.note = note
        self.sender_id = sender_id
        self.receiver_id = receiver_id
    
    def __str__(self):
        return {self.type,self.date,self,self.amount,self.note,self.sender_id,self.receiver_id}