from pydantic import BaseModel
from app.models.pass_field import PassFieldBase
import uuid
from sqlmodel import Field
from datetime import datetime


class PassFieldCreate(PassFieldBase):
    pass_id: uuid.UUID = Field(foreign_key="passmodel.id")


class PassFieldUpdate(PassFieldBase):
    pass


class PassFieldUpdateWithId(PassFieldUpdate):
    id: uuid.UUID


class PassFieldResponse(BaseModel):
    id: uuid.UUID
    key: str
    label: str
    value: str
    field_type: str  # e.g., "secondary_field", "back_field", etc.
    created_at: datetime
    active: bool
