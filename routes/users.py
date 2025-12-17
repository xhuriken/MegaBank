from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from ..db.database import get_session
from ..core.security import decode_token
from ..core.auth import get_current_user
from ..schemas.user import UserPublic
from ..services.user_service import get_user_by_uuid

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserPublic)
def me(user = Depends(get_current_user)):
    return UserPublic(
        uuid=user.uuid,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )