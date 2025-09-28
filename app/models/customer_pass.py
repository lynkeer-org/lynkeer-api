from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, timezone
import uuid
from enum import Enum


class DeviceEnum(str, Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"

class RegistrationMethodEnum(str, Enum):
    QR = "qr"
    MANUAL = "manual"
    LINK = "link"

class CustomerPass(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    pass_id: uuid.UUID = Field(foreign_key="passmodel.id")
    device: DeviceEnum = Field(nullable=False)  # ENUM: ios, android, web
    registration_method: RegistrationMethodEnum = Field(nullable=False)  # ENUM: qr, manual, link
    apple_serial_number: str = Field(default=None)
    apple_authentication_token: str = Field(default=None)
    apple_device_library_id: str = Field(default=None)
    apple_push_token: str = Field(default=None)
    google_id_class: str = Field(default=None)
    google_id_object: str = Field(default=None)
    google_wallet_url: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = Field(default=True)

    __table_args__ = (
        UniqueConstraint("customer_id", "pass_id", name="uq_customer_pass"),
    )


