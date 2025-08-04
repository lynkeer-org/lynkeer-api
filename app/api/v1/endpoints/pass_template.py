from fastapi import APIRouter, Depends, status
from app.core.db import SessionDep
from app.core.security import get_current_user
from app.models.owner import Owner
from app.schemas.pass_template import PassTemplate, PassTemplateResponse
from app.services.pass_model import list_passes_service
from app.services.pass_template import create_pass_template_service
from fastapi import HTTPException

router = APIRouter()


@router.post(
    "/pass-template",
    response_model=PassTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_pass_template(
    pass_template_data: PassTemplate,
    session: SessionDep,
    current_owner: Owner = Depends(get_current_user),
):
    if current_owner.id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Owner ID is missing or unauthorized.",
        )
    return create_pass_template_service(
        pass_template_data, session=session, owner_id=current_owner.id
    )


@router.get("/pass-template", response_model=list[PassTemplateResponse])
async def list_pass_templates(
    session: SessionDep, current_owner: Owner = Depends(get_current_user)
):
    if current_owner.id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Owner ID is missing or unauthorized.",
        )
    return list_passes_service(session, owner_id=current_owner.id)
