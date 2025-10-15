from app.crud.owner import (
    create_owner,
    delete_owner,
    list_owners,
    read_owner,
    update_owner,
)
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate
from app.core.hashing import hash_password
from fastapi import HTTPException, status
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid


def create_owner_service(owner_data: OwnerCreate, session: SessionDep):
    from app.crud.owner import check_email_exists, check_phone_exists
    
    # Validate email uniqueness using the correct session
    if check_email_exists(owner_data.email, session):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered"
        )
    
    # Validate phone uniqueness using the correct session  
    if check_phone_exists(owner_data.phone, session):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Phone already registered"
        )
    
    owner_dict = owner_data.model_dump()
    password = owner_dict.pop("password")  # Get and remove plain password
    owner_dict["password_hash"] = hash_password(password)
    owner = Owner.model_validate(owner_dict)

    return create_owner(owner, session)


def list_owners_service(session: SessionDep):
    return list_owners(session)


def read_owner_service(owner_id: uuid.UUID, session: SessionDep):
    owner_db = read_owner(session=session, owner_id=owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return owner_db


def delete_owner_service(owner_id: uuid.UUID, session: SessionDep):
    owner_db = read_owner(session=session, owner_id=owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )

    return delete_owner(owner_db, session)


def update_owner_service(
    owner_id: uuid.UUID, owner_data: OwnerUpdate, session: SessionDep
):
    owner_db = read_owner(session=session, owner_id=owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )

    return update_owner(owner_db, owner_data, session)
