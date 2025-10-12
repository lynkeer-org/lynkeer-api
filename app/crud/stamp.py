from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlmodel import select
from app.core.db import SessionDep
from app.models.stamp import Stamp
import uuid


def create_stamp(stamp_db: Stamp, session: SessionDep):
    session.add(stamp_db)
    session.flush()
    return stamp_db


def list_stamps(session: SessionDep):
    query = select(Stamp).where(Stamp.active == True)
    return session.exec(query).all()


def read_stamp(stamp_id: uuid.UUID, session: SessionDep):
    stamp_db = session.get(Stamp, stamp_id)
    if not stamp_db or not stamp_db.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stamp does not exist"
        )
    return stamp_db


def read_stamps_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep):
    stamps = session.exec(
        select(Stamp).where(
            Stamp.customer_pass_id == customer_pass_id,
            Stamp.active == True
        )
    ).all()
    return stamps


def delete_stamp(stamp: Stamp, session: SessionDep):
    stamp.active = False  # Mark the stamp as deleted
    session.add(stamp)
    session.flush()
    return {"message": "Stamp deleted successfully"}


def count_active_stamps_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep) -> int:
    """Count the number of active stamps for a specific customer pass"""
    query = select(Stamp).where(
        Stamp.customer_pass_id == customer_pass_id,
        Stamp.active == True
    )
    stamps = session.exec(query).all()
    return len(stamps)


def deactivate_all_stamps_by_customer_pass_id(customer_pass_id: uuid.UUID, session: SessionDep):
    """Set all stamps for a customer pass to active = False"""
    query = select(Stamp).where(
        Stamp.customer_pass_id == customer_pass_id,
        Stamp.active == True
    )
    stamps = session.exec(query).all()
    
    for stamp in stamps:
        stamp.active = False
        session.add(stamp)
    
    session.flush()
    return len(stamps)  # Return number of stamps deactivated
