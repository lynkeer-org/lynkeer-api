import os
from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# sqlite_name = "db.sqlite3"
# sqlite_url = f"sqlite:///{sqlite_name}"

# engine = create_engine(sqlite_url)
# PostgreSQL connection string
# Load environment variables from .env
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

database_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(database_url, echo=True)


@asynccontextmanager
async def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[
    Session, Depends(get_session)
]  # This is a type hint that indicates that the function requires a Session object as a dependency.
