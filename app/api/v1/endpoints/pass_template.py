from fastapi import APIRouter, status
from app.core.db import SessionDep
from app.schemas.pass_template import PassTemplate, PassTemplateResponse
from app.services.pass_template import create_pass_template_service
from app.models.pass_model import PassModel

router = APIRouter()


@router.post(
    "/pass-template",
    response_model=PassTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_pass_template(pass_template_data: PassTemplate, session: SessionDep):
    return create_pass_template_service(pass_template_data, session=session)
