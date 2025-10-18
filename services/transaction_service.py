from sqlmodel import Session
from decimal import Decimal
from ..models.account import Account
from ..models.transaction import Transaction

def transfer(session: Session, *, source_iban: str, target_iban: str, amount: Decimal) -> Transaction:
    if source_iban == target_iban:
        raise ValueError("Source and target must be different")

    src = session.get(Account, source_iban)
    dst = session.get(Account, target_iban)
    if not src or not dst:
        raise ValueError("Account not found")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if src.balance < amount:
        raise ValueError("Insufficient funds")

    src.balance -= amount
    dst.balance += amount
    tx = Transaction(source_iban=source_iban, target_iban=target_iban, amount=amount)
    session.add_all([src, dst, tx])
    session.commit()
    session.refresh(tx)
    return tx
