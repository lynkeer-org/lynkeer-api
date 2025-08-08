from fastapi import HTTPException, status
from app.core.db import SessionDep
from app.crud.pass_field import read_pass_fields_by_pass_id
from app.models.pass_field import PassField, PassFieldBase
from app.schemas.pass_field import PassFieldCreate, PassFieldResponse, PassFieldUpdate
from app.schemas.pass_model import PassModelResponse, PassUpdate
from app.schemas.pass_template import (
    PassTemplate,
    PassTemplateResponse,
    PassTemplateUpdate,
)
from app.services.pass_field import create_pass_field_service, update_pass_field_service
from app.services.pass_model import (
    create_pass_service,
    list_passes_service,
    read_pass_service,
    update_pass_service,
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
    for field_data in pass_template_data.pass_fields:
        pass_field = PassFieldCreate(
            **field_data.model_dump(), pass_id=created_pass.id  # type: ignore[arg-type]
        )
        create_pass_field_service(pass_field_data=pass_field, session=session)

    # 3. Return the created PassModelpass_fields = read_pass_fields_by_pass_model(created_pass.id, session)
    assert created_pass.id is not None, "created_pass.id is unexpectedly None"
    fields = read_pass_fields_by_pass_id(created_pass.id, session)
    return PassTemplateResponse(
        **created_pass.model_dump(),
        pass_fields=[
            PassFieldResponse.model_validate(field.model_dump()) for field in fields
        ],
    )


def list_passes_template_service(session: SessionDep, owner_id: uuid.UUID):
    # 1. List all PassModels for the owner
    passes = list_passes_service(session=session, owner_id=owner_id)

    # 2. For each PassModel, read the related PassFields
    result = []
    for pass_model in passes:
        if pass_model.id is not None:
            fields = read_pass_fields_by_pass_id(pass_model.id, session)
        else:
            fields = []
        result.append(
            PassTemplateResponse(
                **pass_model.model_dump(),
                pass_fields=[
                    PassFieldResponse.model_validate(field.model_dump())
                    for field in fields
                ],
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
    fields = read_pass_fields_by_pass_id(pass_model.id, session)

    return PassTemplateResponse(
        **pass_model.model_dump(),
        pass_fields=[
            PassFieldResponse.model_validate(field.model_dump()) for field in fields
        ],
    )


def update_pass_template_service(
    pass_id: uuid.UUID,
    pass_template_data: PassTemplateUpdate,
    session: SessionDep,
    owner_id: uuid.UUID,
):
    try:
        # 1. Read the existing PassModel
        pass_db = read_pass_service(pass_id=pass_id, session=session)
        if not pass_db or (pass_db.owner_id != owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pass template does not exist",
            )
        # 2. I get the passupdate data
        pass_update_data = PassUpdate.model_validate(
            pass_template_data.model_dump(exclude={"pass_fields"})
        )
        # 3. Update the PassModel
        updated_pass = update_pass_service(
            pass_id=pass_id, pass_data=pass_update_data, session=session
        )
        # pass_data = PassModelResponse.model_validate(updated_pass.model_dump())
        # 4. Update the PassFields

        for field_data in pass_template_data.pass_fields:
            pass_field_data = PassFieldUpdate.model_validate(
                field_data.model_dump(exclude={"id"})
            )
            update_pass_field_service(
                pass_field_id=field_data.id,
                pass_field_data=pass_field_data,
                session=session,
            )

        fields = read_pass_fields_by_pass_id(pass_id, session)

        response = PassTemplateResponse(
            **updated_pass.model_dump(),
            pass_fields=[
                PassFieldResponse.model_validate(field.model_dump()) for field in fields
            ],
        )
        session.commit()  # Commit the session after all updates
        return response

    except Exception as e:
        session.rollback()  # Rollback the session in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the pass template: {str(e)}",
        )
