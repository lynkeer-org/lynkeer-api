from app.crud.owner import (
    delete_owner,
    list_owners,
    read_owner,
    update_owner,
)
from app.schemas.owner import OwnerUpdate
from app.models.owner import Owner
from fastapi import APIRouter, status
from app.core.db import SessionDep
from app.services.owner import list_owners_service, read_owner_service

router = APIRouter()


@router.get("/owners", response_model=list[Owner], tags=["owners"])
async def list_owners_endpoint(session: SessionDep):
    return list_owners_service(session)


@router.get("/owners/{owner_id}", response_model=Owner, tags=["owners"])
async def read_owner_endpoint(owner_id: int, session: SessionDep):
    return read_owner_service(session=session, owner_id=owner_id)


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
