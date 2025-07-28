from fastapi import HTTPException, status
from app.crud.pass_field import (
    create_pass_field,
    delete_pass_field,
    list_pass_fields,
    read_pass_field,
    update_pass_field,
)
from app.crud.pass_model import read_pass
from app.models.pass_field import PassField
from app.schemas.pass_field import PassFieldCreate, PassFieldUpdate
from app.core.db import SessionDep
import uuid


def create_pass_field_service(pass_field_data: PassFieldCreate, session: SessionDep):
    pass_field_data_dict = pass_field_data.model_dump()
    pass_id_raw = pass_field_data_dict.get(
        "pass_id"
    )  # Get the owner_id from the pass_data_dict
    if not pass_id_raw:  # Check if owner_id is provided
        raise HTTPException(status_code=400, detail="pass_id is required")

    try:
        pass_id: uuid.UUID = pass_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for owner_id")

    pass_model = read_pass(
        session=session, pass_id=pass_id
    )  # Retrieve the owner using the owner_id
    if not pass_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )
    if not pass_model.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Pass is not active"
        )

    pass_field = PassField.model_validate(pass_field_data_dict)
    return create_pass_field(pass_field, session)


def list_pass_fields_service(session: SessionDep):
    return list_pass_fields(session)


def read_pass_field_service(pass_field_id: uuid.UUID, session: SessionDep):
    pass_field_db = read_pass_field(session=session, pass_field_id=pass_field_id)
    if not pass_field_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The pass field does not exist",
        )
    return pass_field_db


def update_pass_field_service(
    pass_field_id: uuid.UUID, pass_field_data: PassFieldUpdate, session: SessionDep
):
    pass_field_db = read_pass_field(session=session, pass_field_id=pass_field_id)
    if not pass_field_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The pass field does not exist",
        )

    return update_pass_field(pass_field_db, pass_field_data, session)


def delete_pass_field_service(pass_field_id: uuid.UUID, session: SessionDep):
    pass_field_db = read_pass_field(session=session, pass_field_id=pass_field_id)
    if not pass_field_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The pass field does not exist",
        )

    return delete_pass_field(pass_field_db, session)
