from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.core.db import SessionDep
import uuid

from app.crud.pass_field import read_pass_fields_by_pass_id
from app.models.pass_model import PassModel
from app.schemas.pass_model import PassUpdate
from app.models.pass_field import PassField, PassFieldBase
from app.schemas.pass_template import PassTemplateResponse


def create_pass(pass_model_db: PassModel, session: SessionDep):
    session.add(pass_model_db)
    session.commit()
    session.refresh(pass_model_db)

    return pass_model_db


def list_passes(session: SessionDep, owner_id: uuid.UUID):
    # Get all passes and include their fields

    query = select(PassModel).where(
        PassModel.owner_id == owner_id, PassModel.active == True
    )
    passes = session.exec(query).all()
    return passes


def read_pass(pass_id: uuid.UUID, session: SessionDep):
    pass_db = session.get(PassModel, pass_id)
    if not pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return pass_db


def delete_pass(pass_model: PassModel, session: SessionDep):
    pass_model.active = False  # Mark the owner as deleted
    session.add(pass_model)
    session.commit()
    session.refresh(pass_model)

    return {"message": "pass deleted successfully"}


def update_pass(pass_model: PassModel, pass_data: PassUpdate, session: SessionDep):
    pass_data_dict = pass_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    pass_model.sqlmodel_update(pass_data_dict)
    session.add(pass_model)
    session.flush()
    # session.commit()
    session.refresh(pass_model)
    return pass_model
