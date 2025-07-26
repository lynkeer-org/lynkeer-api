from app.core.db import SessionDep
from app.crud.pass_type import (
    create_pass_type,
    delete_pass_type,
    list_pass_types,
    read_pass_type,
    update_pass_type,
)
from app.models.pass_type import PassType
from app.schemas.pass_type import PassTypeCreate, PassTypeUpdate
import uuid
from fastapi import HTTPException, status


def create_pass_type_service(pass_type_data: PassTypeCreate, session: SessionDep):
    pass_type_dict = pass_type_data.model_dump()
    pass_type = PassType.model_validate(pass_type_dict)

    return create_pass_type(pass_type, session)


def list_pass_types_service(session: SessionDep):
    return list_pass_types(session)


def read_pass_type_service(pass_type_id: uuid.UUID, session: SessionDep):
    pass_type_db = read_pass_type(session=session, pass_type_id=pass_type_id)
    if not pass_type_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The pass type does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return pass_type_db


def update_pass_type_service(
    pass_type_id: uuid.UUID, pass_type_data: PassTypeUpdate, session: SessionDep
):
    pass_type_db = read_pass_type(session=session, pass_type_id=pass_type_id)
    if not pass_type_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The pass type does not exist"
        )

    return update_pass_type(pass_type_db, pass_type_data, session)


def delete_pass_type_service(pass_type_id: uuid.UUID, session: SessionDep):
    pass_type_db = read_pass_type(session=session, pass_type_id=pass_type_id)
    if not pass_type_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The pass type does not exist"
        )

    return delete_pass_type(pass_type_db, session)
