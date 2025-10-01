from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from sqlalchemy import Column, UniqueConstraint, Index, text
from sqlalchemy.dialects.postgresql import CITEXT
from app.models.customer_pass import CustomerPass
import uuid

from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from app.models.owner import Owner
    from app.models.pass_type import PassType
    from app.models.pass_field import PassField
    from app.models.customer import Customer    
    


class PassBase(SQLModel):
    
    title: str = Field(sa_column=Column(CITEXT(), nullable=False))
    stamp_goal: int = Field(default=None)
    logo_url: str = Field(default=None)
    text_color: str = Field(default=None)
    background_color: str = Field(default=None)
    google_class_id: str = Field(default=None)
    apple_pass_type_identifier: str = Field(default=None)

    @field_validator("stamp_goal")
    @classmethod
    def validate_stamp_goal(cls, value):
        if value is not None and value <= 1:
            raise ValueError("stamp_goal must be greater than 1")
        return value


class PassModel(PassBase, table=True):

    __table_args__ = (
        Index(
            "uq_active_title_owner_type",
            "title", "owner_id", "pass_type_id",
            unique=True,
            postgresql_where=text("active = true"),
        ),
    )
   
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    owner_id: uuid.UUID = Field(foreign_key="owner.id", nullable=False)
    owner: "Owner" = Relationship(back_populates="passes")
    fields: list["PassField"] = Relationship(back_populates="pass_model")
    pass_type_id: uuid.UUID = Field(foreign_key="passtype.id", nullable=False)
    pass_type: "PassType" = Relationship(back_populates="passes")
    customers: list['Customer']= Relationship(back_populates='passes', link_model=CustomerPass)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True, nullable=False)
