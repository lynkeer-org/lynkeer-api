from models.owner import Owner, OwnerCreate, OwnerResponse, OwnerUpdate
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from utils.hashing import hash_password

router = APIRouter()


@router.post(
    "/sign-up",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["owners"],
)
async def create_owner(owner_data: OwnerCreate, session: SessionDep):

    owner_dict = owner_data.model_dump()
    password = owner_dict.pop("password")  # Get and remove plain password
    owner_dict["password_hash"] = hash_password(password)
    owner = Owner.model_validate(owner_dict)
    session.add(owner)
    session.commit()
    session.refresh(owner)

    return owner


@router.get("/owners", response_model=list[Owner], tags=["owners"])
async def list_owners(session: SessionDep):
    # This query selects all customers from the database and returns them as a list.
    return session.exec(select(Owner)).all()


@router.get("/owners/{owner_id}", response_model=Owner, tags=["owners"])
async def read_owner(owner_id: int, session: SessionDep):
    owner_db = session.get(Owner, owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    # This function retrieves a customer from the database using the provided customer_id.
    return owner_db


@router.delete("/owners/{owner_id}", tags=["owners"])
async def delete_owner(owner_id: int, session: SessionDep):
    owner_db = session.get(Owner, owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    session.delete(owner_db)
    session.commit()
    return {"message": "Owner deleted successfully"}


@router.patch(
    "/owners/{owner_id}",
    response_model=Owner,
    status_code=status.HTTP_201_CREATED,
    tags=["owners"],
)
async def update_owner(owner_id: int, owner_data: OwnerUpdate, session: SessionDep):
    owner_db = session.get(Owner, owner_id)
    if not owner_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner does not exist"
        )
    owner_data_dict = owner_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True option is used to exclude unset fields from the dictionary
    owner_db.sqlmodel_update(owner_data_dict)
    session.add(owner_db)
    session.commit()
    session.refresh(owner_db)
    return owner_db
