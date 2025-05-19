from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.core.hashing import verify_password
from app.core.security import create_access_token
from app.crud.owner import create_owner
from app.models.owner import Owner
from app.schemas.owner import OwnerLogin, OwnerCreate, OwnerResponse
from app.core.db import SessionDep


router = APIRouter()


@router.post(
    "/signup", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED
)
async def create_owner_endpoint(owner_data: OwnerCreate, session: SessionDep):
    return create_owner(session=session, owner_data=owner_data)


@router.post("/signin")
def login_owner(login_data: OwnerLogin, session: SessionDep):
    query = select(Owner).where(Owner.email == login_data.email)
    owner = session.exec(query).first()

    if not owner or not verify_password(login_data.password, owner.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(owner.id)})
    return {"access_token": token, "token_type": "bearer"}
