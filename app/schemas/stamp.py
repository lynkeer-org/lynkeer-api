from pydantic import BaseModel
from datetime import datetime
import uuid


class StampCreate(BaseModel):
    customer_pass_id: uuid.UUID


class StampResponse(BaseModel):
    id: uuid.UUID
    customer_pass_id: uuid.UUID
    issued_at: datetime
    active: bool