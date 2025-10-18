from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..core.auth import get_current_user_uuid
from ..schemas.transaction import TransferCreate
from ..services.account_service import get_account_by_iban
from ..services.transaction_service import transfer

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("")
def make_transfer(body: TransferCreate, session: Session = Depends(get_session), user_uuid: str = Depends(get_current_user_uuid)):
    # vérifier propriété du compte source
    src = get_account_by_iban(session, body.source_iban)
    if not src or src.user_uuid != user_uuid:
        raise HTTPException(status_code=404, detail="Source account not found")

    # le compte cible doit exister (peut être un autre utilisateur)
    dst = get_account_by_iban(session, body.target_iban)
    if not dst:
        raise HTTPException(status_code=404, detail="Target account not found")

    try:
        tx = transfer(session, source_iban=body.source_iban, target_iban=body.target_iban, amount=body.amount)
        return {"id": tx.id, "source_iban": tx.source_iban, "target_iban": tx.target_iban, "amount": str(tx.amount), "date": tx.created_at}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
