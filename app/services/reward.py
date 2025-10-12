from fastapi import HTTPException, status
from app.crud.reward import (
    create_reward,
    delete_reward,
    list_rewards,
    read_reward,
    read_rewards_by_customer_pass_id,
)
from app.crud.customer_pass import read_customer_pass
from app.crud.pass_model import read_pass
from app.models.reward import Reward
from app.schemas.reward import RewardCreate
from app.core.db import SessionDep
import uuid


def create_reward_service(reward_data: RewardCreate, session: SessionDep, owner_id: uuid.UUID):
    reward_data_dict = reward_data.model_dump()
    
    # Validate customer_pass_id
    customer_pass_id = reward_data_dict.get("customer_pass_id")
    customer_pass = read_customer_pass(customer_pass_id=customer_pass_id, session=session)
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    if not customer_pass.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CustomerPass is not active"
        )

    # Owner validation: Ensure the customer pass belongs to owner's pass template
    pass_model = read_pass(customer_pass.pass_id, session)
    if pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only create rewards for your own pass templates"
        )

    reward = Reward.model_validate(reward_data_dict)
    return create_reward(reward, session)


def list_rewards_service(session: SessionDep):
    return list_rewards(session)


def read_reward_service(reward_id: uuid.UUID, session: SessionDep):
    reward_db = read_reward(reward_id=reward_id, session=session)
    if not reward_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The reward does not exist",
        )
    return reward_db


def read_rewards_by_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep):
    # Validate that the customer_pass exists
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    
    return read_rewards_by_customer_pass_id(customer_pass_id=customer_pass_id, session=session)


def delete_reward_service(reward_id: uuid.UUID, session: SessionDep):
    reward_db = read_reward(reward_id=reward_id, session=session)
    if not reward_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The reward does not exist",
        )

    return delete_reward(reward_db, session)
