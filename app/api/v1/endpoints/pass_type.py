from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter

from app.core.db import SessionDep
from app.models.pass_type import PassType
from app.schemas.pass_type import PassTypeCreate
from app.services.pass_type import create_pass_type_service, list_pass_types_service


router = APIRouter()


@router.post(
    "/types-passes",
    response_model=PassType,
    status_code=status.HTTP_201_CREATED,
    tags=["types-passes"],
)
async def create_pass_type(pass_type_data: PassTypeCreate, session: SessionDep):
    return create_pass_type_service(pass_type_data=pass_type_data, session=session)


@router.get("/types-passes", response_model=list[PassType], tags=["types-passes"])
async def list_pass_endpoint(session: SessionDep):
    return list_pass_types_service(session)
