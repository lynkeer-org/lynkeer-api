from pydantic import BaseModel
from sqlmodel import Field
from datetime import datetime
import uuid


class RewardCreate(BaseModel):
    customer_pass_id: uuid.UUID = Field(foreign_key="customerpass.id", nullable=False)


class RewardResponse(BaseModel):
    id: uuid.UUID
    customer_pass_id: uuid.UUID
    claimed_at: datetime | None  # None when reward is issued, datetime when claimed
    issued_at: datetime  # When the reward was issued
    active: bool