import jwt
from fastapi import HTTPException, Depends
from sqlmodel import Session

from ..database import engine
from ..models.user import User
from .generate_token import secret_key, algorithm
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()
# secret_key = "j'aime le caca"
# algorithm = "HS256"

def get_user(authorization: HTTPAuthorizationCredentials = Depends (bearer_scheme)):
    try:
        payload = jwt.decode(authorization.credentials, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")


def get_current_user(payload: dict = Depends(get_user)):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
        return user