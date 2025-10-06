from fastapi import APIRouter, status, Depends
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.core.db import SessionDep
from app.services.customer import (
    create_customer_service,
    get_customer_by_email_service,
    update_customer_service,
    delete_customer_service,
)
from app.core.security import get_current_user_or_apikey, get_current_user
import uuid

router = APIRouter()


@router.post(
    "/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_endpoint(
    customer_data: CustomerCreate,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    owner_id = current_owner.id if current_owner is not None else None
    return create_customer_service(customer_data=customer_data, session=session, owner_id=owner_id)


@router.get(
    "/customers/by-email/{email}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
)
async def get_customer_by_email_endpoint(
    email: str,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    owner_id = current_owner.id if current_owner is not None else None
    return get_customer_by_email_service(email=email, session=session, owner_id=owner_id)


@router.patch(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
)
async def update_customer_endpoint(
    customer_id: uuid.UUID,
    customer_data: CustomerUpdate,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    return update_customer_service(
        customer_id=customer_id,
        customer_data=customer_data,
        session=session,
        owner_id=current_user.id,
    )


@router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer_endpoint(
    customer_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    delete_customer_service(
        customer_id=customer_id,
        session=session,
        owner_id=current_owner.id,
    )