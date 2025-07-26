from app.models.pass_field import PassFieldBase
import uuid
from sqlmodel import Field


class PassFieldCreate(PassFieldBase):
    pass_id: uuid.UUID = Field(foreign_key="passmodel.id")


class PassFieldUpdate(PassFieldBase):
    pass
