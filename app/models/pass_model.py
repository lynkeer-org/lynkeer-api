from datetime import datetime, timezone
import uuid
from sqlmodel import Field, Relationship, SQLModel


class PassFieldBase(SQLModel):
    key: str = Field(default=None)
    label: str = Field(default=None)
    value: str = Field(default=None)
    field_type: str = Field(default=None)


class PassField(PassFieldBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    pass_id: uuid.UUID = Field(default=None, foreign_key="pass.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)


class PassTypeBase(SQLModel):
    type: str = Field(default=None)


class PassType(PassTypeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    pass_id: uuid.UUID = Field(default=None, foreign_key="pass.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)


class PassBase(SQLModel):
    title: str = Field(default=None)
    stamp_goal: int = Field(default=None)
    qr_url: str = Field(default=None)
    logo_url: str = Field(default=None)
    text_color: str = Field(default=None)
    background_color: str = Field(default=None)
    google_class_id: str = Field(default=None)
    apple_pass_type_identifier: str = Field(default=None)


class Pass(PassBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    owner_id: uuid.UUID = Field(foreign_key="owner.id")
    owner = Relationship(back_populates="passes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool | None = Field(default=True)
