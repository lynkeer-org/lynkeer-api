from fastapi import HTTPException, status
from app.crud.reward import (
    claim_rewards,
    create_reward,
    delete_reward,
    list_rewards,
    read_reward,
    read_rewards_by_customer_pass_id,
)
from app.crud.customer_pass import read_customer_pass, update_customer_pass
from app.crud.pass_model import read_pass
from app.models.customer_pass import CustomerPass
from app.models.reward import Reward
from app.schemas.customer_pass import CustomerPassUpdate
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


def read_rewards_by_customer_pass_service(customer_pass_id: uuid.UUID, session: SessionDep, owner_id: uuid.UUID):
    # Validate that the customer_pass exists
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    
    # Owner validation: Ensure the customer pass belongs to owner's pass template
    pass_model = read_pass(customer_pass.pass_id, session)
    if pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only access rewards for your own pass templates"
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



def claim_rewards_service(customer_pass_id: uuid.UUID,
        number_of_rewards:int,
        session: SessionDep,
        owner_id: uuid.UUID):
    # Validate that the customer_pass exists
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )

    # Owner validation: Ensure the customer pass belongs to owner's pass template
    pass_model = read_pass(customer_pass.pass_id, session)
    if pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only claim rewards for your own pass templates"
        )
    # Validate that there are enough unclaimed (active) rewards to claim
    available_rewards = read_rewards_by_customer_pass_service(
        customer_pass_id=customer_pass_id, session=session, owner_id=owner_id
    )
    if len(available_rewards) < number_of_rewards:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough rewards available to claim"
        )

    # Claim the rewards (mark as inactive and set claimed_at)
    claimed_rewards = claim_rewards(
        customer_pass_id=customer_pass_id,
        number_of_rewards=number_of_rewards,
        session=session
    )

    # Decrement active_rewards on the customer pass
    new_active_rewards = customer_pass.active_rewards - number_of_rewards
    if new_active_rewards < 0:
        new_active_rewards = 0
    update_data = CustomerPassUpdate(active_rewards=new_active_rewards)
    customer_pass_updated = update_customer_pass(customer_pass, update_data, session)

    return customer_pass_updated
