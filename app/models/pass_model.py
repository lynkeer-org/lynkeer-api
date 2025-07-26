from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Session, select, Relationship
from datetime import datetime, timezone
from app.core.db import engine
import uuid

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.owner import Owner
    from app.models.pass_type import PassType
    from app.models.pass_field import PassField


class PassBase(SQLModel):
    title: str = Field(default=None)
    stamp_goal: int = Field(default=None)
    qr_url: str = Field(default=None)
    logo_url: str = Field(default=None)
    text_color: str = Field(default=None)
    background_color: str = Field(default=None)
    google_class_id: str = Field(default=None)
    apple_pass_type_identifier: str = Field(default=None)

    @field_validator("stamp_goal")
    @classmethod
    def validate_stamp_goal(cls, value):
        if value is not None and value <= 0:
            raise ValueError("stamp_goal must be greater than 0")
        return value


class PassModel(PassBase, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    owner: "Owner" = Relationship(back_populates="passes")
    pass_type_id: uuid.UUID = Field(foreign_key="passtype.id")
    pass_type: "PassType" = Relationship(back_populates="passes")
    fields: list["PassField"] = Relationship(back_populates="pass_model")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)
