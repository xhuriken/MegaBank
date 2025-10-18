from sqlmodel import Session, desc, select
from decimal import Decimal
from typing import Sequence
from ..models.account import Account, AccountState
def open_account(session: Session, *, user_uuid: str, is_primary: bool = False, initial_balance: Decimal = Decimal("0.00")) -> Account:
    account = Account(user_uuid=user_uuid, is_primary=is_primary, balance=initial_balance)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

def get_account_by_iban(session: Session, iban: str) -> Account | None:
    return session.get(Account, iban)


def list_user_accounts(session: Session, user_uuid: str) -> Sequence[Account]:
    return session.exec(
        select(Account)
        .where(Account.user_uuid == user_uuid)
        .order_by(desc(Account.created_at))
    ).all()

def close_account(session: Session, *, iban: str, fallback_iban: str):
    acc = session.get(Account, iban)
    primary = session.get(Account, fallback_iban)
    if not acc or not primary:
        raise ValueError("Account not found")
    if acc.state == AccountState.CLOSED:
        return acc
    if acc.is_primary:
        raise ValueError("Primary account cannot be closed")

    # transfert du solde vers le fallback (compte principal)
    primary.balance += acc.balance
    acc.balance = Decimal("0.00")
    acc.state = AccountState.CLOSED

    session.add_all([acc, primary])
    session.commit()
    session.refresh(acc)
    return acc
