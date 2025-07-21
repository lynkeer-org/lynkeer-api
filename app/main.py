from fastapi import FastAPI

from app.api.v1.endpoints import (
    auth,
    owner,
    pass_model,
)  # This should work if structure is correct
from app import models

from app.core.db import create_all_tables


app = FastAPI(
    lifespan=create_all_tables
)  # This is a FastAPI application instance. The lifespan parameter is used to create and drop the database tables when the application starts and stops.

app.include_router(owner.router)  # This should work if structure is correct
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(pass_model.router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
