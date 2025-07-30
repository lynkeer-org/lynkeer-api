from fastapi import HTTPException, status
from app.core.db import SessionDep
from app.core.hashing import verify_password
from app.core.security import create_access_token
from app.crud.auth import get_owner_by_email
from app.schemas.owner import OwnerLogin


def login_owner_service(login_data: OwnerLogin, session: SessionDep):
    owner = get_owner_by_email(login_data.email, session)

    if not owner or not verify_password(login_data.password, owner.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(owner.id),
            "email": owner.email,
            "name": f"{owner.first_name} {owner.last_name}",
        }
    )
    # return {"access_token": token, "token_type": "bearer"}
    return {
        "token": token,
        "user": {
            "id": str(owner.id),
            "email": owner.email,
            "name": f"{owner.first_name} {owner.last_name}",
        },
    }
