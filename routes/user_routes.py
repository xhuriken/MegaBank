from fastapi import APIRouter, HTTPException
from ..database import engine
from sqlmodel import Session
from ..state import users, typeUserActual
from ..models.user import User, UserDB
from ..schemas.user_schema import UserBody, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: UserBody):
  
    with Session(engine) as session:

     
        existing_user = session.query(UserDB).filter(UserDB.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

       
        new_user = UserDB(
            firstName=user_data.first_name,
            lastName=user_data.last_name,
            email=user_data.email,
            password=user_data.password 
        )

       
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  

        return {
            "message": "New account created!",
            "user_id": new_user.id,
            "first_name": new_user.firstName,
            "last_name": new_user.lastName,
            "email": new_user.email
        }

@router.post("/login")
def login_user(credentials: UserLogin):
    with Session(engine) as session:
        user = session.query(UserDB).filter(UserDB.email == credentials.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Email not found")

        if user.password != credentials.password:  # ⚠️ à hasher plus tard
            raise HTTPException(status_code=401, detail="Invalid password")

        # Stocker l'utilisateur connecté (si tu veux garder ça)
        global typeUserActual
        typeUserActual = user

        return {
            "message": f"Bienvenue {user.firstName}, you're connected!",
            "user": {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email
            }
        }

@router.get("/me")
def user_info(usrId: int):
    with Session(engine) as session:
        user = session.get(UserDB, usrId)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }

 