from fastapi import APIRouter, HTTPException
from ..tresitil import get_acc
from ..models.transaction import *

router = APIRouter(prefix="/transfers", tags=["Transfers"])

#TODO c'est pas transit en fait ? transac ?
@router.post("/")
def transit(amount: float, sender: str, receiver: str):
    if sender == receiver:
        raise HTTPException(400, "Sender and receiver must differ")
    
    s = get_acc(sender)
    r = get_acc(receiver)

    try:
        s.withdraw(amount)
        r.deposit(amount)

        #TODO: save transition.
        #TODO: fonction pour return 1 transaction précise
        #TODO: function pour return toute les transaction d'un compte. (via iban dcp)
        #TODO: bien differentier dépot, transaction, withdraw (Ne pas afficher withdraw dans les fonction toto a faire)
        #TODO: Et ne pas record les transaction de withdraw et depost si elles sont utiliser pour une transition d'argent (ça ferai doublon)

    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return {
        "sender":   {"iban": s.iban, "balance": s.balance},
        "receiver": {"iban": r.iban, "balance": r.balance},
    }

#TODO: pouvoir annuler les transaction !!!!!!!!!!!!!!!!
