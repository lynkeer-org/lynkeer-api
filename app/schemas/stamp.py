from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Field
import uuid


class StampCreate(BaseModel):
    customer_pass_id: uuid.UUID = Field(foreign_key="customerpass.id", nullable=False)


class StampResponse(BaseModel):
    id: uuid.UUID
    customer_pass_id: uuid.UUID
    issued_at: datetime
    active: bool