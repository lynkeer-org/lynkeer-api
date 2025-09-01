from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.models.pass_type import PassType
from app.schemas.pass_type import PassTypeCreate, PassTypeUpdate
from app.services.pass_type import (
    create_pass_type_service,
    delete_pass_type_service,
    list_pass_types_service,
    read_pass_type_service,
    update_pass_type_service,
)
import uuid

router = APIRouter()


@router.post(
    "/types-passes",
    response_model=PassType,
    status_code=status.HTTP_201_CREATED,
)
async def create_pass_type_endpoint(pass_type_data: PassTypeCreate, session: SessionDep):
    return create_pass_type_service(pass_type_data=pass_type_data, session=session)


@router.get("/types-passes", response_model=list[PassType])
async def list_pass_endpoint(session: SessionDep):
    return list_pass_types_service(session)


@router.get("/types-passes/{type_pass_id}", response_model=PassType)
async def read_pass_type_endpoint(pass_type_id: uuid.UUID, session: SessionDep):
    return read_pass_type_service(session=session, pass_type_id=pass_type_id)


@router.patch(
    "/types-passes/{pass_type_id}",
    response_model=PassType,
    status_code=status.HTTP_201_CREATED,
)
async def update_pass_type_endpoint(
    pass_type_id: uuid.UUID, pass_type_data: PassTypeUpdate, session: SessionDep
):
    return update_pass_type_service(
        session=session, pass_type_id=pass_type_id, pass_type_data=pass_type_data
    )


@router.delete(
    "/types-passes/{pass_type_id}",
)
async def delete_pass_type_endpoint(pass_type_id: uuid.UUID, session: SessionDep):
    return delete_pass_type_service(session=session, pass_type_id=pass_type_id)
