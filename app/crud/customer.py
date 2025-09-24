from datetime import datetime, timezone
from sqlmodel import select
from app.models.customer import Customer
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid

def create_customer(customer_db: Customer, session: SessionDep):
    session.add(customer_db)
    session.flush()
    return customer_db

def get_customer_by_email(session: SessionDep, email: str):
    statement = select(Customer).where(Customer.email == email)
    return session.exec(statement).first()

def list_customers(session: SessionDep):
    query = select(Customer).where(Customer.active == True)
    return session.exec(query).all()

def read_customer(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db or not customer_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    return customer_db

def delete_customer(customer: Customer, session: SessionDep):
    customer.active = False  # Mark the customer as deleted
    session.add(customer)
    session.flush()
    return {"message": "Customer deleted successfully"}

def update_customer(customer: Customer, customer_data, session: SessionDep):
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    customer.updated_at = datetime.now(timezone.utc)
    session.add(customer)
    session.flush()
    return customer