from sqlmodel import Session, select, desc
from decimal import Decimal
from models.account import Account
from models.transaction import Transaction


def transfer(
    session: Session,
    *,
    source_iban: str,
    target_iban: str,
    amount: Decimal,
    label: str | None = None
) -> Transaction:
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

    tx = Transaction(
        source_iban=source_iban,
        target_iban=target_iban,
        amount=amount,
        label=label,
    )

    session.add_all([src, dst, tx])
    session.commit()
    session.refresh(tx)
    return tx


def list_transactions_for_account(session: Session, iban: str) -> list[Transaction]:
    stmt = (
        select(Transaction)
        .where(
            (Transaction.source_iban == iban) | (Transaction.target_iban == iban)
        )
        .order_by(desc(Transaction.created_at))
    )
    return list(session.exec(stmt).all())

