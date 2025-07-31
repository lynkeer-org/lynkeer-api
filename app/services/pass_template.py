from app.core.db import SessionDep
from app.crud.pass_field import read_pass_fields_by_pass_id
from app.models.pass_field import PassFieldBase
from app.schemas.pass_field import PassFieldCreate
from app.schemas.pass_template import PassTemplate, PassTemplateResponse
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

    # 3. Return the created PassModelpass_fields = read_pass_fields_by_pass_model(created_pass.id, session)
    assert created_pass.id is not None, "created_pass.id is unexpectedly None"
    pass_fields = read_pass_fields_by_pass_id(created_pass.id, session)
    return PassTemplateResponse(
        **created_pass.model_dump(),
        pass_field=[PassFieldBase.model_validate(field) for field in pass_fields]
    )
