from fastapi import Depends, FastAPI

from app.api.v1.endpoints import (
    auth,
    owner,
    pass_model,
    pass_template,
    pass_type,
)  # This should work if structure is correct

from app.core.db import create_all_tables
from app.core.security import get_current_user


app = FastAPI(
    lifespan=create_all_tables
)  # This is a FastAPI application instance. The lifespan parameter is used to create and drop the database tables when the application starts and stops.

app.include_router(
    owner.router,
    prefix="/api/v1",
    tags=["Owners"],
    dependencies=[Depends(get_current_user)],
)  # This should work if structure is correct
app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Authentication"],
)

app.include_router(
    pass_type.router,
    prefix="/api/v1",
    tags=["Types-passes"],
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    pass_template.router,
    prefix="/api/v1",
    tags=["Pass-templates"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
