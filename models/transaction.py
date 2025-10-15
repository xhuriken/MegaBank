from typing import List, Optional
from sqlmodel import Enum, Field, Relationship, SQLModel

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"

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


class TransactionHistoryDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType
    amount: float
    note: Optional[str] = None

    sender_id: Optional[int] = Field(default=None, foreign_key="accountdb.id")
    receiver_id: Optional[int] = Field(default6=None, foreign_key="accountdb.id")

    # sender_account: Optional["AccountBDD"] = Relationship(back_populates="sent_transactions", sa_relationship_kwargs={"foreign_keys": "[TransactionHistoryBDD.sender_id]"})
    # receiver_account: Optional["AccountBDD"] = Relationship(back_populates="received_transactions", sa_relationship_kwargs={"foreign_keys": "[TransactionHistoryBDD.receiver_id]"})
