from sqlmodel import select
from fastapi import HTTPException, status
from app.core.db import SessionDep
import uuid

from app.models.pass_model import PassModel
from app.schemas.pass_model import PassUpdate


def create_pass(pass_model_db: PassModel, session: SessionDep):
    session.add(pass_model_db)
    session.commit()
    session.refresh(pass_model_db)

    return pass_model_db


def list_passes(session: SessionDep):
    # This query selects all customers from the database and returns them as a list.
    return session.exec(select(PassModel)).all()


def read_pass(pass_id: uuid.UUID, session: SessionDep):
    pass_db = session.get(PassModel, pass_id)
    if not pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return pass_db


def delete_pass(pass_model: PassModel, session: SessionDep):
    session.delete(pass_model)
    session.commit()
    return {"message": "pass deleted successfully"}


def update_pass(pass_model: PassModel, pass_data: PassUpdate, session: SessionDep):
    pass_data_dict = pass_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    pass_model.sqlmodel_update(pass_data_dict)
    session.add(pass_model)
    session.commit()
    session.refresh(pass_model)
    return pass_model
