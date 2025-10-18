from fastapi import APIRouter, HTTPException
from ..utils import get_acc
from ..models.transaction import *
from ..models.user import*
from ..routes.account_routes import *

router = APIRouter(prefix="/transfers", tags=["Transfers"])

#TODO c'est pas transit en fait ? transac ?
@router.post("/")
def transit(amount: int, sender: str, receiver: str):
    if sender == receiver:
        raise HTTPException(400, "Sender and receiver must differ")
    
    s: User = get_acc(sender)
    r: User = get_acc(receiver)

    s.withdraw(amount)
    r.deposit(amount)

        #TODO: save transition.
        #TODO: fonction pour return 1 transaction précise
        #TODO: function pour return toute les transaction d'un compte. (via iban dcp)
        #TODO: bien differentier dépot, transaction, withdraw (Ne pas afficher withdraw dans les fonction toto a faire)
        #TODO: Et ne pas record les transaction de withdraw et depost si elles sont utiliser pour une transition d'argent (ça ferai doublon)
    
    return {
        "sender":   {"iban": s.iban, "balance": s.balance},
        "receiver": {"iban": r.iban, "balance": r.balance},
    }

#TODO: pouvoir annuler les transaction !!!!!!!!!!!!!!!!
