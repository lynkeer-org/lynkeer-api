from fastapi import HTTPException, status
from app.core.db import SessionDep
from app.crud.pass_field import read_pass_fields_by_pass_id
from app.models.pass_field import PassFieldBase
from app.schemas.pass_field import PassFieldCreate
from app.schemas.pass_template import PassTemplate, PassTemplateResponse
from app.services.pass_field import create_pass_field_service
from app.services.pass_model import (
    create_pass_service,
    list_passes_service,
    read_pass_service,
)
import uuid


def create_pass_template_service(
    pass_template_data: PassTemplate, session: SessionDep, owner_id: uuid.UUID
):
    # 1. Create the PassModel
    created_pass = create_pass_service(
        pass_template_data, session=session, owner_id=owner_id
    )

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


def list_passes_template_service(session: SessionDep, owner_id: uuid.UUID):
    # 1. List all PassModels for the owner
    passes = list_passes_service(session=session, owner_id=owner_id)

    # 2. For each PassModel, read the related PassFields
    result = []
    for p in passes:
        if p.id is not None:
            pass_fields = read_pass_fields_by_pass_id(p.id, session)
        else:
            pass_fields = []
        result.append(
            PassTemplateResponse(
                **p.model_dump(),
                pass_field=[PassFieldBase.model_validate(f) for f in pass_fields]
            )
        )

    return result


def read_pass_template_service(
    pass_id: uuid.UUID, session: SessionDep, owner_id: uuid.UUID
):
    # 1. Read the PassModel
    pass_model = read_pass_service(pass_id=pass_id, session=session)
    if not pass_model or (pass_model.owner_id != owner_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass template does not exist"
        )
    # 2. Read the related PassFields
    if pass_model.id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pass ID is missing"
        )
    pass_fields = read_pass_fields_by_pass_id(pass_model.id, session)

    return PassTemplateResponse(
        **pass_model.model_dump(),
        pass_field=[PassFieldBase.model_validate(field) for field in pass_fields]
    )
