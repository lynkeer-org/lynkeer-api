from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Field
import uuid

from app.models.pass_model import PassBase


class PassModelResponse(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    title: str
    stamp_goal: int
    logo_url: str
    text_color: str
    background_color: str
    google_class_id: str
    apple_pass_type_identifier: str
    created_at: datetime
    updated_at: datetime | None = None
    


class PassCreate(PassBase):
    # owner_id: uuid.UUID = Field(foreign_key="owner.id")
    pass_type_id: uuid.UUID = Field(foreign_key="passtype.id")


class PassUpdate(PassBase):
    pass
