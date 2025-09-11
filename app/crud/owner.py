from datetime import datetime, timezone
from sqlmodel import select
from app.models.owner import Owner
from app.schemas.owner import OwnerUpdate
from fastapi import HTTPException, status
from app.core.db import SessionDep
import uuid


def create_owner(owner_db: Owner, session: SessionDep):
    session.add(owner_db)
    session.flush()
    return owner_db


def list_owners(session: SessionDep):
    query = select(Owner).where(Owner.active == True)
    return session.exec(query).all()


def read_owner(owner_id: uuid.UUID, session: SessionDep):
    owner_db = session.get(Owner, owner_id)
    if not owner_db or not owner_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    return owner_db


def delete_owner(owner: Owner, session: SessionDep):
    owner.active = False  # Mark the owner as deleted
    session.add(owner)
    session.flush()

    return {"message": "Owner deleted successfully"}


def update_owner(owner: Owner, owner_data: OwnerUpdate, session: SessionDep):
    owner_data_dict = owner_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    owner.sqlmodel_update(owner_data_dict)
    owner.updated_at = datetime.now(timezone.utc)
    session.add(owner)
    session.flush()

    return owner
