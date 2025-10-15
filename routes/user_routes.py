from fastapi import APIRouter, HTTPException
from ..database import engine
from sqlmodel import Session
from ..datafile import users, typeUserActual
from ..models.user import User
from ..schemas.user_schema import UserBody, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])


#TODO Changer avec un get ??
# il faut pouvoir mettre des param pour choisir le nom email etC...

#TODO merge le token des zouzou kiki et loulou la
#TODO Hash password

@router.post("/register")
def register_user(user_data: UserBody):
    with Session(engine) as session:
     
        existing_user = session.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

       
        new_user = User(
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
        user = session.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Email not found")

        if user.password != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid password")

        # On utilisera plus ça je pense ? ou plus comme ça
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

        #TODO recupérer uniqument les valeurs dont on a besoin pas TOUT le user

        user = session.get(User, usrId)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }

