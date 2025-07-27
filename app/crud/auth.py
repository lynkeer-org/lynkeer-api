from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.owner import Owner


def get_owner_by_email(email: str, session: SessionDep):
    query = select(Owner).where(Owner.email == email)
    owner = session.exec(query).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    return owner
