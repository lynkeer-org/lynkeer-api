from sqlmodel import Field, Relationship, SQLModel
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.pass_model import PassModel


class PassFieldBase(SQLModel):
    key: str = Field(default=None)
    label: str = Field(default=None)
    value: str = Field(default=None)
    field_type: str = Field(default=None)  # e.g., "secondary_field", "back_field", etc.


class PassField(PassFieldBase, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    pass_id: uuid.UUID = Field(foreign_key="passmodel.id")
    pass_model: "PassModel" = Relationship(back_populates="fields")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    nullable=True)
    active: bool | None = Field(default=True)
