import os
from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated, Generator
from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv

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


def get_session() -> Generator[Session, None, None]:
    with Session(engine, expire_on_commit=False) as session:
        yield session


def transactional_session(
    session: Session = Depends(get_session),
) -> Generator[Session, None, None]:
    try:
        yield session
        session.commit()
    except HTTPException:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise


# Use this in endpoints to get automatic commit/rollback
SessionDep = Annotated[Session, Depends(transactional_session)]
