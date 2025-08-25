from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.pass_type import PassType
import uuid

from app.schemas.pass_type import PassTypeUpdate


def create_pass_type(pass_type_db: PassType, session: SessionDep):
    session.add(pass_type_db)
    session.flush()

    return pass_type_db


def read_pass_type(pass_type_id: uuid.UUID, session: SessionDep):
    pass_type_db = session.get(PassType, pass_type_id)
    if not pass_type_db or not pass_type_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="the pass type does not exist"
        )
    return pass_type_db


def list_pass_types(session: SessionDep):
    query = select(PassType).where(PassType.active == True)
    return session.exec(query).all()


def update_pass_type(
    pass_type: PassType, pass_type_data: PassTypeUpdate, session: SessionDep
):
    pass_type_data_dict = pass_type_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    pass_type.sqlmodel_update(pass_type_data_dict)
    session.add(pass_type)
    session.flush()

    return pass_type


def delete_pass_type(pass_type: PassType, session: SessionDep):
    pass_type.active = False  # Mark the owner as deleted
    session.add(pass_type)
    session.flush()

    return {"message": "pass type deleted successfully"}
