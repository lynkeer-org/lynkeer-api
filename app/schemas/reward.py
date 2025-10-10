from pydantic import BaseModel
from datetime import datetime
import uuid


class RewardCreate(BaseModel):
    customer_pass_id: uuid.UUID


class RewardResponse(BaseModel):
    id: uuid.UUID
    customer_pass_id: uuid.UUID
    claimed_at: datetime
    active: bool