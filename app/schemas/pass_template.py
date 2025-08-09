from app.models.pass_field import PassField, PassFieldBase
from app.schemas.pass_field import (
    PassFieldResponse,
    PassFieldUpdate,
    PassFieldUpdateWithId,
)
from app.schemas.pass_model import PassCreate, PassModelResponse, PassUpdate


class PassTemplate(PassCreate):
    pass_fields: list[PassFieldBase]


class PassTemplateUpdate(PassUpdate):
    pass_fields: list[PassFieldUpdateWithId]


class PassTemplateResponse(PassModelResponse):
    pass_fields: list[PassFieldResponse]
