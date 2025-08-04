from fastapi import APIRouter, status
from app.services.auth import login_owner_service
from app.services.owner import create_owner_service
from app.schemas.owner import OwnerLogin, OwnerCreate, OwnerResponse
from app.core.db import SessionDep


router = APIRouter()


@router.post(
    "/sign-up", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED
)
async def create_owner_endpoint(owner_data: OwnerCreate, session: SessionDep):
    return create_owner_service(session=session, owner_data=owner_data)


@router.post("/sign-in")
def login_owner_endpoint(login_data: OwnerLogin, session: SessionDep):

    return login_owner_service(login_data=login_data, session=session)
