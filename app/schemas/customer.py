from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from app.models.customer import CustomerBase
import uuid

class CustomerResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date
    created_at: datetime
    updated_at: datetime | None = None
    active: bool

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date

class CustomerDelete(BaseModel):
    active: bool = False  # Set active to False to mark as deleted