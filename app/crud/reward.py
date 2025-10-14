from fastapi import HTTPException, status
from sqlmodel import func, select
from app.core.db import SessionDep
from app.models.reward import Reward
import uuid


def create_reward(reward_db: Reward, session: SessionDep):
    session.add(reward_db)
    session.flush()
    return reward_db


def list_rewards(session: SessionDep):
    query = select(Reward).where(Reward.active == True)
    rewards = session.exec(query).all()
    return rewards


def read_reward(reward_id: uuid.UUID, session: SessionDep):
    reward_db = session.get(Reward, reward_id)
    if not reward_db or not reward_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward does not exist"
        )
    return reward_db


def read_rewards_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep):
    query =  select(Reward).where(
            Reward.customer_pass_id == customer_pass_id,
            Reward.active == True
        )
    rewards = session.exec(query).all()
    return rewards


def delete_reward(reward: Reward, session: SessionDep):
    reward.active = False  # Mark the reward as deleted
    session.add(reward)
    session.flush()
    return {"message": "Reward deleted successfully"}


def count_active_rewards_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep) -> int:
    """Count the number of active rewards for a specific customer pass"""
    query = select(func.count(Reward.id)).where(
        Reward.customer_pass_id == customer_pass_id,
        Reward.active == True
    )
    result = session.exec(query)
    count = result.one()
    return count or 0
