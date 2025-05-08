from modelsfile import Customer, CustomerCreate, CustomerUpdate
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep

router = APIRouter()


@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(
        customer_data.model_dump()
    )  # model_dump() is used to convert the Pydantic model to a dictionary
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer


@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return session.get(Customer, customer_id)


@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    customer_data_dict = customer_data.model_dump(
        exclude_unset=True
    )  # model_dump() is used to convert the Pydantic model to a dictionary
    # The exclude_unset=True option is used to exclude unset fields from the dictionary
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    # The session.refresh() method is used to refresh the instance from the database
    return customer_db


@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    session.delete(customer_db)
    session.commit()
    return {"message": "Customer deleted successfully"}


@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):
    # This query selects all customers from the database and returns them as a list.
    return session.exec(select(Customer)).all()
