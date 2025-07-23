from app.core.db import SessionDep
from app.crud.pass_type import create_pass_type
from app.models.pass_type import PassType
from app.schemas.pass_type import PassTypeCreate


def create_pass_type_service(pass_type_data: PassTypeCreate, session: SessionDep):
    pass_type_dict = pass_type_data.model_dump()
    pass_type = PassType.model_validate(pass_type_dict)

    return create_pass_type(pass_type, session)
