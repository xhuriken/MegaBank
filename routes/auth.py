from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..services.user_service import register_user, authenticate_user
from ..services.account_service import open_account
from ..schemas.user import UserCreate, UserLogin, UserPublic, AuthResponse, Token
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: UserCreate, session: Session = Depends(get_session)):
    """
    This registers a new user and logs them in immediately.
    We use it as the entry point for user creation; it also opens the primary account.
    """
    try:
        user = register_user(
            session,
            email=body.email,
            password=body.password,
            first_name=body.first_name,
            last_name=body.last_name,
        )

        # Open primary acc for the new user
        open_account(
            session,
            user_uuid=user.uuid,
            is_primary=True,
            initial_balance=Decimal("100.00"),
        )

        # Auto login
        token = authenticate_user(session, email=body.email, password=body.password)

        return {
            "message": "User registered and logged in",
            "user": {
                "uuid": user.uuid,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "access_token": token,
            "token_type": "bearer",
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(body: UserLogin, session: Session = Depends(get_session)):
    """
    This authenticates a user and returns a bearer token.
    We use it as the standard login endpoint for clients.
    """
    try:
        token = authenticate_user(session, email=body.email, password=body.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")