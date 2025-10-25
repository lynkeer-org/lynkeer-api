from fastapi import APIRouter, status, Depends, HTTPException
from app.models.customer_pass import CustomerPass
from app.schemas.customer_pass import CustomerPassResponse
from app.schemas.reward import RewardCreate, RewardResponse
from app.core.db import SessionDep
from app.core.security import get_current_user
from app.models.owner import Owner
from app.services.reward import (
    claim_rewards_service,
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

@router.get(
    "/rewards/claim-reward/{customer_pass_id}",
    response_model=CustomerPassResponse,
    status_code=status.HTTP_200_OK,
)
async def claim_rewards_endpoint(
    customer_pass_id: uuid.UUID,
    number_of_rewards: int,
    session: SessionDep,
    current_owner: Owner = Depends(get_current_user),
):
    if current_owner.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Owner ID is missing or unauthorized.",
        )
    return claim_rewards_service(
        customer_pass_id=customer_pass_id,
        number_of_rewards=number_of_rewards,
        session=session,
        owner_id=current_owner.id
    )
