from sqlmodel import Session, select
from models.beneficiary import Beneficiary


def create_beneficiary(
    session: Session,
    *,
    user_uuid: str,
    name: str,
    iban: str,
) -> Beneficiary:
    if not name:
        raise ValueError("Name is required")

    # optionnel : éviter les doublons (même IBAN pour le même user)
    existing = session.exec(
        select(Beneficiary).where(
            Beneficiary.user_uuid == user_uuid,
            Beneficiary.iban == iban,
        )
    ).first()
    if existing:
        raise ValueError("Beneficiary already exists for this IBAN")

    b = Beneficiary(user_uuid=user_uuid, name=name, iban=iban)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


def list_user_beneficiaries(session: Session, user_uuid: str) -> list[Beneficiary]:
    return list(
        session.exec(
            select(Beneficiary).where(Beneficiary.user_uuid == user_uuid)
        ).all()
    )


def delete_beneficiary(
    session: Session,
    *,
    beneficiary_id: str,
    user_uuid: str,
) -> None:
    b = session.get(Beneficiary, beneficiary_id)
    if not b or b.user_uuid != user_uuid:
        raise ValueError("Beneficiary not found")

    session.delete(b)
    session.commit()
