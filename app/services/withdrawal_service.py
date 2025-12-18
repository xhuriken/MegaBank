from sqlmodel import Session
from decimal import Decimal
from ..models.account import Account
from ..models.withdrawal import Withdrawal

def make_withdrawal(session: Session, *, iban: str, amount: Decimal) -> Withdrawal:
    acc = session.get(Account, iban)
    if not acc:
        raise ValueError("Account not found")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if acc.balance < amount:
        raise ValueError("Insufficient funds")

    acc.balance -= amount
    wd = Withdrawal(account_iban=iban, amount=amount)
    session.add_all([acc, wd])
    session.commit()
    session.refresh(wd)
    return wd
