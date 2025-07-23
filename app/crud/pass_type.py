from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.pass_type import PassType
import uuid


def create_pass_type(pass_type_db: PassType, session: SessionDep):
    session.add(pass_type_db)
    session.commit()
    session.refresh(pass_type_db)
    return pass_type_db


def read_pass_type(pass_type_id: uuid.UUID, session: SessionDep):
    pass_type_db = session.get(PassType, pass_type_id)
    if not pass_type_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return pass_type_db


def list_pass_types(session: SessionDep):
    # This query selects all customers from the database and returns them as a list.
    return session.exec(select(PassType)).all()
