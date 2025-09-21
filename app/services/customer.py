from app.crud.customer import (
    create_customer,
    get_customer_by_email,
    list_customers,
    read_customer,
    update_customer,
    delete_customer,
)
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid

def create_customer_service(customer_data: CustomerCreate, session: SessionDep):
    # Check if email already exists
    if get_customer_by_email(session, customer_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    customer_dict = customer_data.model_dump()
    customer = Customer.model_validate(customer_dict)
    return create_customer(customer, session)

def list_customers_service(session: SessionDep):
    return list_customers(session)

def read_customer_service(customer_id: uuid.UUID, session: SessionDep):
    customer_db = read_customer(customer_id=customer_id, session=session)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    return customer_db

def update_customer_service(
    customer_id: uuid.UUID, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = read_customer(customer_id=customer_id, session=session)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    return update_customer(customer_db, customer_data, session)

def delete_customer_service(customer_id: uuid.UUID, session: SessionDep):
    customer_db = read_customer(customer_id=customer_id, session=session)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    return delete_customer(customer_db, session)