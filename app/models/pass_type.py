from sqlmodel import Field, Relationship, SQLModel
import uuid
from datetime import datetime, timezone
from typing import Optional
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.pass_model import PassModel


class PassTypeBase(SQLModel):
    type: str = Field(default=None)


class PassType(PassTypeBase, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    passes: list["PassModel"] = Relationship(back_populates="pass_type")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    nullable=True)
    active: bool | None = Field(default=True)
