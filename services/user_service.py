from sqlmodel import Session, select
from models.user import User
from sqlmodel import Session, select
from models.user import User
from core.security import hash_password, verify_password, create_access_token

def register_user(session: Session, *, email: str, password: str, first_name: str, last_name: str) -> User:
    """
    This creates a new user with a hashed password.
    We use it during /auth/register before opening the primary account.
    """
    if session.exec(select(User).where(User.email == email)).first():
        raise ValueError("Email already exists")
    user = User(email=email, password_hash=hash_password(password), first_name=first_name, last_name=last_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, *, email: str, password: str) -> str:
    """
    This checks credentials and returns a JWT.
    We use it in /auth/login and after /auth/register for auto-login.
    """
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    # sub = UUID, pas d'email
    return create_access_token(sub=user.uuid)


def get_user_by_uuid(session: Session, uuid: str) -> User | None:
    return session.get(User, uuid)
