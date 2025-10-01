from datetime import datetime, timezone
from sqlmodel import select
from app.models.customer_pass import CustomerPass
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid

def create_customer_pass(customer_pass_db: CustomerPass, session: SessionDep):
    session.add(customer_pass_db)
    session.flush()
    return customer_pass_db

def read_customer_pass(customer_pass_id: uuid.UUID, session: SessionDep):
    customer_pass_db = session.get(CustomerPass, customer_pass_id)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CustomerPass does not exist",
        )
    return customer_pass_db

def list_customer_passes(session: SessionDep):
    query = select(CustomerPass)
    return session.exec(query).all()

def update_customer_pass(customer_pass: CustomerPass, customer_pass_data, session: SessionDep):
    customer_pass_data_dict = customer_pass_data.model_dump(exclude_unset=True)
    customer_pass.sqlmodel_update(customer_pass_data_dict)
    customer_pass.updated_at = datetime.now(timezone.utc)
    session.add(customer_pass)
    session.flush()
    return customer_pass

def delete_customer_pass(customer_pass: CustomerPass, session: SessionDep):
    customer_pass.active = False  # Mark the CustomerPass as inactive
    session.add(customer_pass)
    session.flush()
    return {"message": "CustomerPass deleted successfully"}