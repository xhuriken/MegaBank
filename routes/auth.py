from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..schemas.user import UserCreate, UserLogin, UserPublic
from ..services.user_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, status_code=201)
def register(body: UserCreate, session: Session = Depends(get_session)):
    try:
        user = register_user(session, email=body.email, password=body.password, first_name=body.first_name, last_name=body.last_name)
        return UserPublic(uuid=user.uuid, email=user.email, first_name=user.first_name, last_name=user.last_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(body: UserLogin, session: Session = Depends(get_session)):
    try:
        token = authenticate_user(session, email=body.email, password=body.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
