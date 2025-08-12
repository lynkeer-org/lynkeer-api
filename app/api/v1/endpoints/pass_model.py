from fastapi import APIRouter, status
from app.schemas.pass_model import PassCreate, PassUpdate
from app.core.db import SessionDep
from app.models.pass_model import PassModel

from app.schemas.pass_model import PassModelResponse
from app.services.pass_model import (
    create_pass_service,
    delete_pass_service,
    list_passes_service,
    read_pass_service,
    update_pass_service,
)
import uuid

router = APIRouter()


@router.get("/passes/{pass_id}", response_model=PassModel)
async def read_pass_endpoint(pass_id: uuid.UUID, session: SessionDep):
    return read_pass_service(session=session, pass_id=pass_id)


@router.patch(
    "/passes/{pass_id}", response_model=PassModel, status_code=status.HTTP_201_CREATED
)
async def update_pass_endpoint(
    pass_id: uuid.UUID, pass_data: PassUpdate, session: SessionDep
):
    return update_pass_service(session=session, pass_id=pass_id, pass_data=pass_data)


@router.delete("/passes/{pass_id}")
async def delete_pass_endpoint(pass_id: uuid.UUID, session: SessionDep):
    return delete_pass_service(session=session, pass_id=pass_id)
