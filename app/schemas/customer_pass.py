from pydantic import BaseModel
from datetime import datetime
from app.models.customer_pass import CustomerPassBase
import uuid

class CustomerPassResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    pass_id: uuid.UUID
    device: str
    registration_method: str
    apple_serial_number: str | None = None
    apple_authentication_token: str | None = None
    apple_device_library_id: str | None = None
    apple_push_token: str | None = None
    google_id_class: str | None = None
    google_id_object: str | None = None
    google_wallet_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    active: bool

class CustomerPassCreate(CustomerPassBase):
    pass

class CustomerPassUpdate(BaseModel):
    device: str | None = None
    registration_method: str | None = None
    apple_serial_number: str | None = None
    apple_authentication_token: str | None = None
    apple_device_library_id: str | None = None
    apple_push_token: str | None = None
    google_id_class: str | None = None
    google_id_object: str | None = None
    google_wallet_url: str | None = None
    active: bool | None = None