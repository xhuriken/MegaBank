from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from ..db.database import get_session
from ..core.security import decode_token
from ..schemas.user import UserPublic
from ..services.user_service import get_user_by_uuid

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_uuid(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_token(token)
    return payload["sub"]

@router.get("/me", response_model=UserPublic)
def me(session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    user = get_user_by_uuid(session, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic(uuid=user.uuid, email=user.email, first_name=user.first_name, last_name=user.last_name)
