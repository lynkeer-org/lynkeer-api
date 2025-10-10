from fastapi import HTTPException, status
from app.crud.stamp import (
    create_stamp,
    delete_stamp,
    list_stamps,
    read_stamp,
    read_stamps_by_customer_pass_id,
)
from app.crud.customer_pass import read_customer_pass
from app.models.stamp import Stamp
from app.schemas.stamp import StampCreate
from app.core.db import SessionDep
import uuid


def create_stamp_service(stamp_data: StampCreate, session: SessionDep, owner_id: uuid.UUID | None = None):
    stamp_data_dict = stamp_data.model_dump()
    customer_pass_id_raw = stamp_data_dict.get("customer_pass_id")
    
    if not customer_pass_id_raw:
        raise HTTPException(status_code=400, detail="customer_pass_id is required")

    try:
        customer_pass_id: uuid.UUID = customer_pass_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for customer_pass_id")

    # Validate that the customer_pass exists and is active
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    if not customer_pass.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CustomerPass is not active"
        )

    # Owner validation: If authenticated with Bearer token, validate ownership through pass template
    if owner_id is not None:
        # Need to import and read the pass to check owner
        from app.crud.pass_model import read_pass
        pass_model = read_pass(customer_pass.pass_id, session)
        if pass_model.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You can only create stamps for customer passes from your own pass templates"
            )

    stamp = Stamp.model_validate(stamp_data_dict)
    return create_stamp(stamp, session)


def list_stamps_service(session: SessionDep, owner_id: uuid.UUID | None = None):
    if owner_id is not None:
        # Filter stamps by owner through customer_pass -> pass_model relationship
        from sqlmodel import select
        from app.models.customer_pass import CustomerPass
        from app.models.pass_model import PassModel
        
        query = (
            select(Stamp)
            .join(CustomerPass, Stamp.customer_pass_id == CustomerPass.id)
            .join(PassModel, CustomerPass.pass_id == PassModel.id)
            .where(
                Stamp.active == True,
                CustomerPass.active == True,
                PassModel.active == True,
                PassModel.owner_id == owner_id
            )
        )
        return session.exec(query).all()
    else:
        return list_stamps(session)


def read_stamp_service(stamp_id: uuid.UUID, session: SessionDep):
    stamp_db = read_stamp(stamp_id=stamp_id, session=session)
    if not stamp_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The stamp does not exist",
        )
    return stamp_db


def read_stamps_by_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    # Validate that the customer_pass exists
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    
    return read_stamps_by_customer_pass_id(customer_pass_id=customer_pass_id, session=session)


def delete_stamp_service(stamp_id: uuid.UUID, session: SessionDep):
    stamp_db = read_stamp(stamp_id=stamp_id, session=session)
    if not stamp_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The stamp does not exist",
        )

    return delete_stamp(stamp_db, session)
