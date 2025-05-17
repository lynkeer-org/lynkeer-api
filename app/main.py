from fastapi import FastAPI

from api.v1.endpoints import owner  # This should work if structure is correct

from db import create_all_tables


app = FastAPI(
    lifespan=create_all_tables
)  # This is a FastAPI application instance. The lifespan parameter is used to create and drop the database tables when the application starts and stops.

app.include_router(owner.router)  # This should work if structure is correct


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
