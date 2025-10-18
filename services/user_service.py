from sqlmodel import Session, select
from ..models.user import User
from ..core.security import hash_password, verify_password, create_access_token

def register_user(session: Session, *, email: str, password: str, first_name: str, last_name: str) -> User:
    if session.exec(select(User).where(User.email == email)).first():
        raise ValueError("Email already exists")
    user = User(email=email, password_hash=hash_password(password), first_name=first_name, last_name=last_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, *, email: str, password: str) -> str:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise ValueError("Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    return create_access_token(sub=user.uuid)

def get_user_by_uuid(session: Session, uuid: str) -> User | None:
    return session.get(User, uuid)
