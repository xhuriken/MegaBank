import jwt
from fastapi import HTTPException

from security.generate_token import *
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

def verify_token(authorization: HTTPAuthorizationCredentials = Depends (bearer_scheme)):
    try:
        payload = jwt.decode(authorization.data, secret_key, algorithm=algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")