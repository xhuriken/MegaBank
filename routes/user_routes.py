from fastapi import APIRouter, HTTPException
from ..state import *
from ..models.user import User
from ..schemas.user_schema import UserBody, UserLogin
from ..security.generate_token import generate_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: UserBody):
    new_id = max(users.keys()) + 1

    for u in users.values():
        if u.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already exist")

    new_user = User(
        id=new_id,
        firstName=user_data.first_name,
        lastName=user_data.last_name,
        email=user_data.email,
        password=user_data.password 
    )

    users[new_id] = new_user

    return {
        "message": "New account created !",
        "first_name": new_user.firstName,
        "last_name": new_user.lastName
    }

@router.post("/login")
def login_user(credentials: UserLogin):
    global userAcutal

    for u in users.values():
        if u.email == credentials.email and u.password == credentials.password:
            typeUserActual = u
            token = generate_token(u)
           
            return {
                "message": f"Bienvenue {u.firstName}, You're connected",
                "user": typeUserActual,
                "token": token
            }

    raise HTTPException(status_code=401, detail="Bad credentials")

@router.get("/me")
def user_info(usrId: int):
    for i in users.values():
        if(i.id == usrId):
            return {"First Name: " : i.firstName, "Last Name" : i.lastName, "Email" : i.email}
    return {
        "message": "user not found !"
    }
 