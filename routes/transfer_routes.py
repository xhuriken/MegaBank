from fastapi import APIRouter, HTTPException
from ..utils import get_acc

router = APIRouter(prefix="/transfers", tags=["Transfers"])

@router.post("/")
def transit(amount: float, sender: str, receiver: str):
    if sender == receiver:
        raise HTTPException(400, "Sender and receiver must differ")
    
    s = get_acc(sender)
    r = get_acc(receiver)

    try:
        s.withdraw(amount)
        r.deposit(amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return {
        "sender":   {"iban": s.iban, "balance": s.balance},
        "receiver": {"iban": r.iban, "balance": r.balance},
    }
