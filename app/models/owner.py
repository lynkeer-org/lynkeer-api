from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.pass_model import PassModel


class OwnerBase(SQLModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field(default=None)  # Use EmailStr for validation
    phone: str = Field(default=None)




class Owner(OwnerBase, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    password_hash: str = Field(default=None)
    passes: list["PassModel"] = Relationship(back_populates="owner")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    nullable=True)
    active: bool = Field(default=True)
