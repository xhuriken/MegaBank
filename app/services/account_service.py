from sqlmodel import Session, desc, select
from sqlalchemy import func
from typing import cast
from decimal import Decimal
from typing import Sequence, Tuple
from ..models.account import Account, AccountState

MAX_ACCOUNTS_PER_USER = 5

"""
This counts how many accounts a user owns.
We use it to enforce the 5-accounts-per-user limit when opening a new account.
"""
def count_user_accounts(session: Session, user_uuid: str) -> int:
    return int(
        session.exec(
            select(func.count())
            .select_from(Account)
            .where(Account.user_uuid == user_uuid)
        ).one()
    )

def has_primary_account(session: Session, user_uuid: str) -> bool:
    return session.exec(
        select(Account).where(
            Account.user_uuid == user_uuid,
            Account.is_primary == True  # noqa: E712
        )
    ).first() is not None

def open_account(
        session: Session,
        *,
        user_uuid: str,
        is_primary: bool = False,
        initial_balance: Decimal = Decimal("0.00"),
        account_name: str | None = None 
    ) -> Account:

    # max 5 account
    if count_user_accounts(session, user_uuid) >= MAX_ACCOUNTS_PER_USER:
        raise ValueError("Account limit reached (5)")
    # one primary acc per user
    if is_primary and has_primary_account(session, user_uuid):
        raise ValueError("User already has a primary account")

    if is_primary:
        final_name = "Compte courant"
    else:
        if not account_name:
            raise ValueError("Account name is required for non-primary accounts")
        final_name = account_name

    account = Account(
        user_uuid=user_uuid,
        is_primary=is_primary,
        balance=initial_balance,
        name=final_name,
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

def get_account_by_iban(session: Session, iban: str) -> Account | None:
    return session.get(Account, iban)


# TODO: don't show closed acc
def list_user_accounts(session: Session, user_uuid: str) -> Sequence[Account]:
    return session.exec(
        select(Account)
        .where(
            Account.user_uuid == user_uuid,
            Account.state != AccountState.CLOSED,  # on enlève les "closed"
        )
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

    # transfer balance to primary balance
    primary.balance += acc.balance
    acc.balance = Decimal("0.00")
    acc.state = AccountState.CLOSED

    session.add_all([acc, primary])
    session.commit()
    session.refresh(acc)
    return acc
