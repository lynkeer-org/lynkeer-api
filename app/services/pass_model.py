from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid
from app.crud.owner import read_owner
from app.crud.pass_model import (
    create_pass,
    delete_pass,
    list_passes,
    read_pass,
    update_pass,
)
from app.crud.pass_type import read_pass_type
from app.schemas.pass_model import PassCreate, PassUpdate
from app.models.pass_model import PassModel


def create_pass_service(
    pass_data: PassCreate, session: SessionDep, owner_id: uuid.UUID
):
    pass_data_dict = pass_data.model_dump()
    owner = read_owner(session=session, owner_id=owner_id)
    if not owner:  # Check if owner_id is provided
        raise HTTPException(status_code=400, detail="Owner not found")

    if not owner.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Owner is not active"
        )
    # Validate the pass_type_id
    pass_type_id_raw = pass_data_dict.get("pass_type_id")
    if not pass_type_id_raw:
        raise HTTPException(status_code=400, detail="pass_type_id is required")
    try:
        pass_type_id: uuid.UUID = pass_type_id_raw
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid UUID format for pass_type_id"
        )
    pass_type = read_pass_type(
        session=session, pass_type_id=pass_type_id
    )  # Retrieve the pass_type using the pass_type_id
    if not pass_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass type does not exist"
        )
    pass_data_dict["owner_id"] = owner_id
    pass_model = PassModel.model_validate(pass_data_dict)
    return create_pass(pass_model, session)


def list_passes_service(session: SessionDep, owner_id: uuid.UUID):
    return list_passes(session, owner_id=owner_id)


def read_pass_service(pass_id: uuid.UUID, session: SessionDep):
    pass_db = read_pass(session=session, pass_id=pass_id)
    if not pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return pass_db


def delete_pass_service(pass_id: uuid.UUID, session: SessionDep):
    pass_db = read_pass(session=session, pass_id=pass_id)
    if not pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )

    return delete_pass(pass_db, session)


def update_pass_service(pass_id: uuid.UUID, pass_data: PassUpdate, session: SessionDep):
    pass_db = read_pass(session=session, pass_id=pass_id)
    if not pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )

    return update_pass(pass_db, pass_data, session)
