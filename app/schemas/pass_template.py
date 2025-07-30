from app.models.pass_field import PassFieldBase
from app.schemas.pass_model import PassCreate


class PassTemplate(PassCreate):
    pass_field: list[PassFieldBase] = []
