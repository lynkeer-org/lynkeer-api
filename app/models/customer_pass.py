from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, timezone
import uuid
from enum import Enum

if TYPE_CHECKING:
    from app.models.stamp import Stamp
    from app.models.reward import Reward


class DeviceEnum(str, Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"

class RegistrationMethodEnum(str, Enum):
    QR = "qr"
    MANUAL = "manual"
    LINK = "link"

class CustomerPassBase(SQLModel):
    device: DeviceEnum = Field(nullable=False)
    registration_method: RegistrationMethodEnum = Field(nullable=False)
    apple_serial_number: str | None = Field(default=None)
    apple_authentication_token: str | None = Field(default=None)
    apple_device_library_id: str | None = Field(default=None)
    apple_push_token: str | None = Field(default=None)
    google_id_class: str | None = Field(default=None)
    google_id_object: str | None = Field(default=None)
    google_wallet_url: str | None = Field(default=None)
    customer_id: uuid.UUID = Field(foreign_key="customer.id", nullable=False)
    pass_id: uuid.UUID = Field(foreign_key="passmodel.id", nullable=False)

class CustomerPass(CustomerPassBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    active: bool = Field(default=True)
    stamps: list["Stamp"] = Relationship(back_populates="customer_pass")
    rewards: list["Reward"] = Relationship(back_populates="customer_pass")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("customer_id", "pass_id", name="uq_customer_pass"),
    )


