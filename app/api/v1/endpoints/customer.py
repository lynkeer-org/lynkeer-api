from fastapi import APIRouter, status, Depends
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.core.db import SessionDep
from app.services.customer import create_customer_service
from app.core.security import get_current_user_or_apikey

router = APIRouter()

@router.post(
    "/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_endpoint(
    customer_data: CustomerCreate,
    session: SessionDep,
    current_user = Depends(get_current_user_or_apikey)
):
    return create_customer_service(session=session, customer_data=customer_data)