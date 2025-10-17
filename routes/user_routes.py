import jwt
from fastapi import APIRouter, HTTPException, Depends

from ..security.hash_password import hash_password, verify_password
from ..security.generate_token import generate_token
from ..database import engine
from sqlmodel import Session
from ..datafile import users, typeUserActual
from ..models.user import User
from ..schemas.user_schema import UserBody, UserLogin
from ..security.verify_token import get_user, get_current_user
from ..routes.account_routes import open_account

router = APIRouter(prefix="/users", tags=["Users"])


#TODO Changer avec un get ??
# il faut pouvoir mettre des param pour choisir le nom email etC...

@router.post("/register")
def register_user(user_data: UserBody):
    with Session(engine) as session:
     
        existing_user = session.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

               #TODO REACT select nationality

        new_user = User(
            nationality=user_data.nationality,
            firstName=user_data.first_name,
            lastName=user_data.last_name,
            email=user_data.email,
            password=hash_password(user_data.password),
        )

       
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        
        userlogin = UserLogin(email=user_data.email, password=user_data.password)
        
        login_user(userlogin)
        
        # open_account(new_user.id)

        return {
            "message": "New account created!",
            "user_id": new_user.id,
            "user_nationlity": new_user.nationality,
            "first_name": new_user.firstName,
            "last_name": new_user.lastName,
            "email": new_user.email
        }

@router.post("/login")
def login_user(credentials: UserLogin):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Email not found")

        if not verify_password(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = generate_token(user)
        print(token)
        return {
            "message": f"Bienvenue {user.firstName}, you're connected!",
            "user": {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email
            },
            "token": token
        }


@router.get("/me")
def user_info(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:

        user = session.get(User, current_user.id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }

@router.get("/testtoken")
def test_token(payload: dict = Depends(get_user)):
    print("Payload reçu :", payload)
    user_id = payload["id"]
    return {"message": f"Bienvenue utilisateur {user_id}, ton token est valide"}