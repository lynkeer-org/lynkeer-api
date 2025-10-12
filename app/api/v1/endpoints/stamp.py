from fastapi import APIRouter, status, Depends
from app.schemas.stamp import StampCreate, StampResponse
from app.core.db import SessionDep
from app.core.security import get_current_user_or_apikey, get_current_user
from app.services.stamp import read_stamps_by_customer_pass_service
from app.services.stamp import (
    create_stamp_service,
    list_stamps_service,
    read_stamp_service,
    delete_stamp_service,
)
import uuid

router = APIRouter()


@router.post(
    "/stamps",
    response_model=StampResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stamp_endpoint(
    stamp_data: StampCreate,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    # Extract owner_id from current_owner (None if API key authentication)
    owner_id = current_owner.id if current_owner is not None else None
    
    return create_stamp_service(
        stamp_data=stamp_data, session=session, owner_id=owner_id
    )


@router.get(
    "/stamps",
    response_model=list[StampResponse],
    status_code=status.HTTP_200_OK,
)
async def list_stamps_endpoint(
    session: SessionDep, current_user=Depends(get_current_user)
):
    return list_stamps_service(session=session, owner_id=current_user.id)


@router.get(
    "/stamps/{stamp_id}",
    response_model=StampResponse,
    status_code=status.HTTP_200_OK,
)
async def read_stamp_endpoint(
    stamp_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    return read_stamp_service(
        stamp_id=stamp_id, session=session
    )


@router.get(
    "/customer-passes/stamps/by-customer-pass/{customer_pass_id}",
    response_model=list[StampResponse],
    status_code=status.HTTP_200_OK,
)
async def list_stamps_by_customer_pass_endpoint(
    customer_pass_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user_or_apikey),
):
    
    return read_stamps_by_customer_pass_service(customer_pass_id=customer_pass_id, session=session)


@router.delete(
    "/stamps/{stamp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_stamp_endpoint(
    stamp_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    delete_stamp_service(
        stamp_id=stamp_id, session=session
    )
