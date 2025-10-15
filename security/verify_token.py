import jwt
from fastapi import HTTPException, Depends
from sqlmodel import Session

from ..models.account import Account
from ..database import engine
from ..models.user import User
from .generate_token import secret_key, algorithm
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

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

#TODO: faire une fonction pour vérifier si l'iban demandé appartien bien à l'utilisateur connecté avec le token

# def is_iban_belongs_to_user(iban: str, authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> bool:
#
#     try:
#         payload = jwt.decode(authorization.credentials, secret_key, algorithms=[algorithm])
#         user_id = payload.get("id")
#
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token: missing user id")
#
#         with Session(engine) as session:
#             account = session.query(Account).filter(Account.iban == iban).first()
#
#             if not account:
#                 return False
#
#             return account.user_id == user_id
#
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expiré")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Token invalide")
