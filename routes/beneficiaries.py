from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..core.auth import get_current_user_uuid
from ..schemas.beneficiary import BeneficiaryCreate, BeneficiaryPublic
from ..services.beneficiary_service import (
    create_beneficiary,
    list_user_beneficiaries,
    delete_beneficiary,
)

router = APIRouter(
    prefix="/beneficiaries",
    tags=["beneficiaries"],
)


@router.post("", response_model=BeneficiaryPublic, status_code=201)
def create_my_beneficiary(
    body: BeneficiaryCreate,
    session: Session = Depends(get_session),
    user_uuid: str = Depends(get_current_user_uuid),
):
    try:
        b = create_beneficiary(
            session,
            user_uuid=user_uuid,
            name=body.name,
            iban=body.iban,
        )
        return BeneficiaryPublic(
            id=b.id,
            user_uuid=b.user_uuid,
            name=b.name,
            iban=b.iban,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[BeneficiaryPublic])
def my_beneficiaries(
    session: Session = Depends(get_session),
    user_uuid: str = Depends(get_current_user_uuid),
):
    bs = list_user_beneficiaries(session, user_uuid)
    return [
        BeneficiaryPublic(
            id=b.id,
            user_uuid=b.user_uuid,
            name=b.name,
            iban=b.iban,
        )
        for b in bs
    ]


@router.delete("/{beneficiary_id}", status_code=204)
def remove_beneficiary(
    beneficiary_id: str,
    session: Session = Depends(get_session),
    user_uuid: str = Depends(get_current_user_uuid),
):
    try:
        delete_beneficiary(
            session,
            beneficiary_id=beneficiary_id,
            user_uuid=user_uuid,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
