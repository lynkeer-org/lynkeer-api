from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Session, select, Relationship
from datetime import datetime, timezone
from app.core.db import engine
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.owner import Owner


class PassBase(SQLModel):
    title: str = Field(default=None)
    stamp_goal: int = Field(default=None)
    qr_url: str = Field(default=None)
    logo_url: str = Field(default=None)
    text_color: str = Field(default=None)
    background_color: str = Field(default=None)
    google_class_id: str = Field(default=None)
    apple_pass_type_identifier: str = Field(default=None)


class PassModel(PassBase, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    owner: "Owner" = Relationship(back_populates="passes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)
