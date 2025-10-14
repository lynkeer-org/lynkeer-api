from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.stamp import StampCreate, StampResponse
from app.core.db import SessionDep
from app.core.security import get_current_user
from app.services.stamp import (
    create_stamp_service,
    
)


router = APIRouter()


@router.post(
    "/stamps",
    response_model=StampResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stamp_endpoint(
    stamp_data: StampCreate,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    if current_owner.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Owner ID is missing or unauthorized.",
        )
   
    
    return create_stamp_service(
        stamp_data=stamp_data, session=session, owner_id=current_owner.id
    )


