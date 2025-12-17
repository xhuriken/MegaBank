from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from .security import decode_token
from ..db.database import get_session
from ..services.user_service import get_user_by_uuid

bearer_scheme = HTTPBearer()

def get_current_user_uuid(
    cred: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    try:
        payload = decode_token(cred.credentials)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(
    session: Session = Depends(get_session),
    user_uuid: str = Depends(get_current_user_uuid),
):
    user = get_user_by_uuid(session, user_uuid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
