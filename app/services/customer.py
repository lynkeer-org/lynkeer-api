from app.crud.customer import create_customer
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.core.db import SessionDep
from fastapi import HTTPException, status
import uuid

def create_customer_service(customer_data: CustomerCreate, session: SessionDep):
    customer_dict = customer_data.model_dump()
    customer = Customer.model_validate(customer_dict)
    return create_customer(customer, session)