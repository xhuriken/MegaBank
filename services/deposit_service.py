from sqlmodel import Session
from decimal import Decimal
from models.account import Account
from models.deposit import Deposit

def make_deposit(session: Session, *, iban: str, amount: Decimal) -> Deposit:
    acc = session.get(Account, iban)
    if not acc:
        raise ValueError("Account not found")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    acc.balance += amount
    dep = Deposit(account_iban=iban, amount=amount)
    session.add_all([acc, dep])
    session.commit()
    session.refresh(dep)
    return dep
