from app.models.pass_field import PassFieldBase
from app.schemas.pass_model import PassCreate, PassModelResponse


class PassTemplate(PassCreate):
    pass_field: list[PassFieldBase]


class PassTemplateResponse(PassModelResponse):
    pass_field: list[PassFieldBase]
