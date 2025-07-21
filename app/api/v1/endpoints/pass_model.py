from fastapi import APIRouter, HTTPException, status
from app.crud.owner import read_owner
from app.models.owner import Owner
from app.schemas.pass_model import PassCreate
from app.core.db import SessionDep
from app.models.pass_model import PassModel
from sqlmodel import Field
from app.models.pass_model import PassBase

from app.schemas.pass_model import PassModelResponse
from app.services.owner import list_owners_service
from app.services.pass_model import create_pass_service, list_passes_service

router = APIRouter()


@router.post(
    "/passes",
    response_model=PassModelResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["passes"],
)
async def create_pass(pass_data: PassCreate, session: SessionDep):
    return create_pass_service(pass_data=pass_data, session=session)


@router.get("/passes", response_model=list[PassModel], tags=["passes"])
async def list_passes_endpoint(session: SessionDep):
    return list_passes_service(session)
