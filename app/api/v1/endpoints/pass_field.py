from fastapi import APIRouter, HTTPException, status
from app.core.db import SessionDep
from app.models.pass_field import PassField
from app.schemas.pass_field import PassFieldCreate, PassFieldUpdate
from app.services.pass_field import (
    create_pass_field_service,
    delete_pass_field_service,
    list_pass_fields_service,
    read_pass_field_service,
    update_pass_field_service,
)
import uuid


router = APIRouter()


@router.post(
    "/pass-fields",
    response_model=PassField,
    status_code=status.HTTP_201_CREATED,
    tags=["pass-fields"],
)
async def create_pass_field_endpoint(
    pass_field_data: PassFieldCreate, session: SessionDep
):
    return create_pass_field_service(pass_field_data=pass_field_data, session=session)


@router.get("/pass-fields", response_model=list[PassField], tags=["pass-fields"])
async def list_pass_fields_endpoint(session: SessionDep):
    return list_pass_fields_service(session)


@router.patch(
    "/pass-fields/{pass_field_id}",
    response_model=PassField,
    status_code=status.HTTP_201_CREATED,
    tags=["pass-fields"],
)
async def update_pass_field_endpoint(
    pass_field_id: uuid.UUID, pass_field_data: PassFieldUpdate, session: SessionDep
):
    return update_pass_field_service(
        session=session, pass_field_id=pass_field_id, pass_field_data=pass_field_data
    )


@router.get(
    "/pass-fields/{pass_field_id}", response_model=PassField, tags=["pass-fields"]
)
async def read_pass_field_endpoint(pass_field_id: uuid.UUID, session: SessionDep):
    return read_pass_field_service(session=session, pass_field_id=pass_field_id)


@router.delete("/pass-fields/{pass_field_id}", tags=["pass-fields"])
async def delete_pass_field_endpoint(pass_field_id: uuid.UUID, session: SessionDep):
    return delete_pass_field_service(session=session, pass_field_id=pass_field_id)
