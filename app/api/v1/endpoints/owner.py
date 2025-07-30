from app.crud.owner import (
    delete_owner,
    list_owners,
    read_owner,
    update_owner,
)
from app.models.pass_model import PassModel
from app.schemas.owner import OwnerUpdate
from app.models.owner import Owner
from fastapi import APIRouter, HTTPException, status
from app.core.db import SessionDep
from app.services.owner import (
    delete_owner_service,
    list_owners_service,
    read_owner_service,
    update_owner_service,
)
import uuid

router = APIRouter()


@router.get("/owners", response_model=list[Owner])
async def list_owners_endpoint(session: SessionDep):
    return list_owners_service(session)


@router.get("/owners/{owner_id}", response_model=Owner)
async def read_owner_endpoint(owner_id: uuid.UUID, session: SessionDep):
    return read_owner_service(session=session, owner_id=owner_id)


@router.delete("/owners/{owner_id}")
async def delete_owner_endpoint(owner_id: uuid.UUID, session: SessionDep):
    return delete_owner_service(session=session, owner_id=owner_id)


@router.patch(
    "/owners/{owner_id}",
    response_model=Owner,
    status_code=status.HTTP_201_CREATED,
)
async def update_owner_endpoint(
    owner_id: uuid.UUID, owner_data: OwnerUpdate, session: SessionDep
):
    return update_owner_service(
        session=session, owner_id=owner_id, owner_data=owner_data
    )


@router.get("/owners/{owner_id}/passes", response_model=list[PassModel])
async def get_owner_passes_endpoint(owner_id: uuid.UUID, session: SessionDep):
    owner = read_owner_service(session=session, owner_id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    return owner.passes  # Assuming 'passes' is a relationship in the Owner model
