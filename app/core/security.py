from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.security import OAuth2, OAuth2PasswordBearer
from app.core.config import settings
from datetime import timezone
from app.core.db import SessionDep

from app.crud.owner import read_owner

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/sign-in")
# oauth2_scheme = APIKeyHeader(name="Authorization")
# Secret key & algorithm from config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class OAuth2PasswordBearerWithBearerOnly(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=tokenUrl))
        super().__init__(flows=flows)

    async def __call__(self, request):
        authorization = request.headers.get("Authorization")
        if authorization is None:
            raise HTTPException(status_code=401, detail="No autorizado")
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="No autorizado")
        return param


# Usa esta clase personalizada
# oauth2_scheme = OAuth2PasswordBearerWithBearerOnly(tokenUrl="/api/v1/sign-in")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        owner = read_owner(session=session, owner_id=user_id)
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found or inactive")
        return owner

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
