from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid
import jwt
from .config import (
    JWT_SECRET, JWT_ALG, ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_LEEWAY_SECONDS, JWT_ISS, JWT_AUD
)

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

def create_access_token(
    *, sub: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    scope: Optional[str] = None, with_jti: bool = False
) -> str:
    now = _utcnow()
    exp = now + timedelta(minutes=expires_minutes)

    payload: Dict[str, Any] = {
        "sub": sub,            # user
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "iss": JWT_ISS,       
        "aud": JWT_AUD,       
    }
    if scope:
        payload["scope"] = scope
    if with_jti:
        payload["jti"] = str(uuid.uuid4())

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALG],
        leeway=JWT_LEEWAY_SECONDS,
        options={"require": ["sub", "exp", "iat"]},
        audience=JWT_AUD,  
        issuer=JWT_ISS,    
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)
