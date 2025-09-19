from app.models.customer import Customer
from app.core.db import SessionDep

def create_customer(customer_db: Customer, session: SessionDep):
    session.add(customer_db)
    session.flush()
    return customer_db