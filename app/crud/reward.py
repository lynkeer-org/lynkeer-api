from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.reward import Reward
import uuid


def create_reward(reward_db: Reward, session: SessionDep):
    session.add(reward_db)
    session.flush()
    return reward_db


def list_rewards(session: SessionDep):
    query = select(Reward).where(Reward.active == True)
    return session.exec(query).all()


def read_reward(reward_id: uuid.UUID, session: SessionDep):
    reward_db = session.get(Reward, reward_id)
    if not reward_db or not reward_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward does not exist"
        )
    return reward_db


def read_rewards_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep):
    rewards = session.exec(
        select(Reward).where(
            Reward.customer_pass_id == customer_pass_id,
            Reward.active == True
        )
    ).all()
    return rewards


def delete_reward(reward: Reward, session: SessionDep):
    reward.active = False  # Mark the reward as deleted
    session.add(reward)
    session.flush()
    return {"message": "Reward deleted successfully"}
