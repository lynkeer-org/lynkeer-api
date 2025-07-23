from pydantic import BaseModel, EmailStr
from datetime import datetime

from sqlmodel import Field
from app.models.owner import OwnerBase
import uuid

from app.models.pass_model import PassBase


class PassModelResponse(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    title: str
    stamp_goal: int
    qr_url: str
    logo_url: str
    text_color: str
    background_color: str
    google_class_id: str
    apple_pass_type_identifier: str


class PassCreate(PassBase):
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    pass_type_id: uuid.UUID = Field(foreign_key="passtype.id")


class PassUpdate(PassBase):
    pass
