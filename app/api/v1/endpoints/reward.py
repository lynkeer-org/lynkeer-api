from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.reward import RewardCreate, RewardResponse
from app.core.db import SessionDep
from app.core.security import get_current_user
from app.models.owner import Owner
from app.services.reward import (
    create_reward_service,
    read_rewards_by_customer_pass_service,
)
import uuid

router = APIRouter()


@router.post(
    "/rewards",
    response_model=RewardResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_reward_endpoint(
    reward_data: RewardCreate,
    session: SessionDep,
    current_owner: Owner = Depends(get_current_user),
):
    if current_owner.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Owner ID is missing or unauthorized.",
        )
    return create_reward_service(
        reward_data=reward_data, session=session, owner_id=current_owner.id
    )


