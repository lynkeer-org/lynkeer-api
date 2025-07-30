from app.core.db import SessionDep
from app.schemas.pass_field import PassFieldCreate
from app.schemas.pass_template import PassTemplate
from app.services.pass_field import create_pass_field_service
from app.services.pass_model import create_pass_service


def create_pass_template_service(pass_template_data: PassTemplate, session: SessionDep):
    # 1. Create the PassModel
    created_pass = create_pass_service(pass_template_data, session=session)

    # 2. Create the related PassFields
    for field_data in pass_template_data.pass_field:
        pass_field = PassFieldCreate(
            **field_data.model_dump(), pass_id=created_pass.id  # type: ignore[arg-type]
        )
        create_pass_field_service(pass_field_data=pass_field, session=session)

    return created_pass
