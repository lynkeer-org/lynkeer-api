from app.crud.customer_pass import (
    create_customer_pass,
    read_customer_pass,
    list_customer_passes,
    update_customer_pass,
    delete_customer_pass,
)
from app.models.customer_pass import CustomerPass
from app.schemas.customer_pass import CustomerPassCreate, CustomerPassUpdate
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid

def create_customer_pass_service(customer_pass_data: CustomerPassCreate, session: SessionDep):
    customer_pass_dict = customer_pass_data.model_dump()
    customer_pass = CustomerPass.model_validate(customer_pass_dict)
    return create_customer_pass(customer_pass, session)

def list_customer_passes_service(session: SessionDep):
    return list_customer_passes(session)

def read_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    return customer_pass_db

def update_customer_pass_service(
    customer_pass_id: uuid.UUID, customer_pass_data: CustomerPassUpdate, session: SessionDep
):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    return update_customer_pass(customer_pass_db, customer_pass_data, session)

def delete_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    return delete_customer_pass(customer_pass_db, session)