from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.pass_field import PassField
import uuid

from app.schemas.pass_field import PassFieldUpdate


def create_pass_field(pass_field_db: PassField, session: SessionDep):
    session.add(pass_field_db)
    session.flush()

    return pass_field_db


def list_pass_fields(session: SessionDep):
    return session.exec(select(PassField)).all()


def read_pass_field(pass_field_id: uuid.UUID, session: SessionDep):
    pass_field_db = session.get(PassField, pass_field_id)
    if not pass_field_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass field does not exist"
        )
    return pass_field_db


def read_pass_fields_by_pass_id(pass_id: uuid.UUID, session: SessionDep):
    pass_fields = session.exec(
        select(PassField).where(PassField.pass_id == pass_id)
    ).all()
    if not pass_fields:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pass fields found for this pass",
        )
    return pass_fields


def update_pass_field(
    pass_field: PassField, pass_field_data: PassFieldUpdate, session: SessionDep
):
    pass_field_data_dict = pass_field_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    pass_field.sqlmodel_update(pass_field_data_dict)
    session.add(pass_field)
    session.flush()

    return pass_field


def delete_pass_field(pass_field: PassField, session: SessionDep):
    pass_field.active = False  # Mark the pass field as deleted
    session.add(pass_field)
    session.flush()

    return {"message": "Pass field deleted successfully"}
