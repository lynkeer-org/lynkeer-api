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
from app.crud.customer import get_customer_by_email
import uuid

def create_customer_service(customer_data: CustomerCreate, session: SessionDep, owner_id: uuid.UUID | None = None):
    # Check if email already exists in customer table
    existing_customer = get_customer_by_email(session, customer_data.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Customer email already registered"
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
    customer_id: uuid.UUID, customer_data: CustomerUpdate, session: SessionDep, owner_id: uuid.UUID
):
    customer_db = read_customer(customer_id=customer_id, session=session)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    
    # Owner validation: Check if customer has passes from the authenticated owner
    
    customer_with_passes = get_customer_by_email(session, customer_db.email, owner_id)
    if not customer_with_passes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update customers who have passes from your pass templates"
        )
    
    return update_customer(customer_db, customer_data, session)

def delete_customer_service(customer_id: uuid.UUID, session: SessionDep, owner_id: uuid.UUID):
    customer_db = read_customer(customer_id=customer_id, session=session)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    
    # Owner validation: Check if customer has passes from the authenticated owner
    customer_with_passes = get_customer_by_email(session, customer_db.email, owner_id)
    if not customer_with_passes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete customers who have passes from your pass templates"
        )
    
    return delete_customer(customer_db, session)

def get_customer_by_email_service(email: str, session: SessionDep, owner_id: uuid.UUID | None = None):
    customer = get_customer_by_email(session=session, email=email, owner_id=owner_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer