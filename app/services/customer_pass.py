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
from app.crud.customer import read_customer
from app.crud.pass_model import read_pass

def create_customer_pass_service(customer_pass_data: CustomerPassCreate, session: SessionDep, owner_id: uuid.UUID | None = None):
    customer_pass_dict = customer_pass_data.model_dump()

    # Validate customer_id
    customer_id = customer_pass_dict.get("customer_id")
    customer = read_customer(customer_id=customer_id, session=session)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )

    # Validate pass_id
    pass_id = customer_pass_dict.get("pass_id")
    pass_model = read_pass(pass_id=pass_id, session=session)
    if not pass_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass does not exist"
        )
    
    # Owner validation: If authenticated with Bearer token, ensure pass belongs to the owner
    if owner_id is not None and pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only create customer passes for your own pass templates"
        )

    customer_pass = CustomerPass.model_validate(customer_pass_dict)
    return create_customer_pass(customer_pass, session)

def list_customer_passes_service(session: SessionDep, owner_id: uuid.UUID):
    return list_customer_passes(session, owner_id)

def read_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    return customer_pass_db

def update_customer_pass_service(
    customer_pass_id: uuid.UUID, customer_pass_data: CustomerPassUpdate, session: SessionDep, owner_id: uuid.UUID
):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    
    # Owner validation: Ensure the customer pass belongs to owner's pass template
    from app.crud.pass_model import read_pass
    pass_model = read_pass(customer_pass_db.pass_id, session)
    if pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only update customer passes for your own pass templates"
        )
    
    return update_customer_pass(customer_pass_db, customer_pass_data, session)

def delete_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    customer_pass_db = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    return delete_customer_pass(customer_pass_db, session)