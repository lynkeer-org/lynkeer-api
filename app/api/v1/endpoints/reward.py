from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.reward import RewardCreate, RewardResponse
from app.core.db import SessionDep
from app.core.security import get_current_user
from app.models.owner import Owner
from app.services.reward import read_rewards_by_customer_pass_service
from app.services.reward import (
    create_reward_service,
    list_rewards_service,
    read_reward_service,
    delete_reward_service,
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
    "/rewards",
    response_model=list[RewardResponse],
    status_code=status.HTTP_200_OK,
)
async def list_rewards_endpoint(
    session: SessionDep, current_owner=Depends(get_current_user)
):
    return list_rewards_service(session=session, owner_id=current_owner.id)


@router.get(
    "/rewards/{reward_id}",
    response_model=RewardResponse,
    status_code=status.HTTP_200_OK,
)
async def read_reward_endpoint(
    reward_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    return read_reward_service(
        reward_id=reward_id, session=session, owner_id=current_owner.id
    )


@router.get(
    "/customer-passes/rewards/by-customer-pass/{customer_pass_id}",
    response_model=list[RewardResponse],
    status_code=status.HTTP_200_OK,
)
async def list_rewards_by_customer_pass_endpoint(
    customer_pass_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    
    return read_rewards_by_customer_pass_service(customer_pass_id=customer_pass_id, session=session, owner_id=current_owner.id)


@router.delete(
    "/rewards/{reward_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reward_endpoint(
    reward_id: uuid.UUID,
    session: SessionDep,
    current_owner=Depends(get_current_user),
):
    delete_reward_service(
        reward_id=reward_id, session=session, owner_id=current_owner.id
    )