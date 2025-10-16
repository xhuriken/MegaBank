from fastapi import APIRouter, HTTPException
from ..models.beneficiary import Beneficiary
from ..datafile import *
from ..database import engine
from sqlmodel import Session

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])

@router.get("/create")
def create_beneficiary(userId: int, name: str, iban: str):
    with Session(engine) as session:

        #TODO make function for check user existance ? we will use it a LITTLE PARTOUT

        user = session.query(User).filter(User.id == userId).first()
        if not user:
            raise HTTPException(status_code=400, detail="User doesn't exist")


        if not session.query(Account).filter(Account.iban == iban).first():
            raise HTTPException(status_code=400, detail="Iban doesn't exist")

        #TODO if name null dont add it !!!!!!
        #TODO pour le kiff mettre le name par defaut le nom de l'user a qui appartient l'iban ?
        new_beneficiary = Beneficiary(name=name, iban=iban, userid=userId)

        #TODO idk if is bien but niggeur faire une method qui fait le add commit refresh tout seul avec en param l'objet a commit genre t'a kpté

        session.add(new_beneficiary)
        session.commit()
        session.refresh(new_beneficiary)  

        #TODO IN ENGLISH PLEASE
        return {
            "message": f"Bénéficiaire '{name}' (IBAN: {iban}) ajouté pour l'utilisateur ID {userId}.",
        }