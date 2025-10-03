from fastapi import APIRouter, status, Depends
from app.schemas.customer_pass import CustomerPassCreate, CustomerPassResponse, CustomerPassUpdate
from app.core.db import SessionDep
from app.core.security import get_current_user_or_apikey, get_current_user
from app.services.customer_pass import (
    create_customer_pass_service,
    list_customer_passes_service,
    read_customer_pass_service,
    update_customer_pass_service,
    delete_customer_pass_service,
)
import uuid

router = APIRouter()


@router.post(
    "/customer-passes",
    response_model=CustomerPassResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_pass_endpoint(
    customer_pass_data: CustomerPassCreate,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    # Extract owner_id from current_owner (None if API key authentication)
    owner_id = current_owner.id if current_owner is not None else None
    
    return create_customer_pass_service(
        customer_pass_data=customer_pass_data, session=session, owner_id=owner_id
    )


@router.get(
    "/customer-passes",
    response_model=list[CustomerPassResponse],
    status_code=status.HTTP_200_OK,
)
async def list_customer_passes_endpoint(
    session: SessionDep, current_user=Depends(get_current_user)
):
    return list_customer_passes_service(session=session, owner_id=current_user.id)


@router.get(
    "/customer-passes/{customer_pass_id}",
    response_model=CustomerPassResponse,
    status_code=status.HTTP_200_OK,
)
async def read_customer_pass_endpoint(
    customer_pass_id: uuid.UUID,
    session: SessionDep,
    current_user=Depends(get_current_user_or_apikey),
):
    return read_customer_pass_service(
        customer_pass_id=customer_pass_id, session=session
    )


@router.patch(
    "/customer-passes/{customer_pass_id}",
    response_model=CustomerPassResponse,
    status_code=status.HTTP_200_OK,
)
async def update_customer_pass_endpoint(
    customer_pass_id: uuid.UUID,
    customer_pass_data: CustomerPassUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    return update_customer_pass_service(
        customer_pass_id=customer_pass_id,
        customer_pass_data=customer_pass_data,
        session=session,
        owner_id=current_user.id,
    )


@router.delete(
    "/customer-passes/{customer_pass_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer_pass_endpoint(
    customer_pass_id: uuid.UUID,
    session: SessionDep,
    current_user=Depends(get_current_user_or_apikey),
):
    delete_customer_pass_service(
        customer_pass_id=customer_pass_id, session=session
    )