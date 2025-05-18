from app.crud.owner import (
    create_owner,
    delete_owner,
    list_owners,
    read_owner,
    update_owner,
)
from app.schemas.owner import OwnerCreate, OwnerResponse, OwnerUpdate
from app.models.owner import Owner
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.core.hashing import hash_password

router = APIRouter()


@router.get("/owners", response_model=list[Owner], tags=["owners"])
async def list_owners_endpoint(session: SessionDep):
    return list_owners(session)


@router.get("/owners/{owner_id}", response_model=Owner, tags=["owners"])
async def read_owner_endpoint(owner_id: int, session: SessionDep):
    return read_owner(session=session, owner_id=owner_id)


@router.delete("/owners/{owner_id}", tags=["owners"])
async def delete_owner_endpoint(owner_id: int, session: SessionDep):
    return delete_owner(session=session, owner_id=owner_id)


@router.patch(
    "/owners/{owner_id}",
    response_model=Owner,
    status_code=status.HTTP_201_CREATED,
    tags=["owners"],
)
async def update_owner_endpoint(
    owner_id: int, owner_data: OwnerUpdate, session: SessionDep
):
    return update_owner(session=session, owner_id=owner_id, owner_data=owner_data)
