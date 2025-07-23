from app.core.db import SessionDep
from app.models.pass_type import PassType


def create_pass_type(pass_type_db: PassType, session: SessionDep):
    session.add(pass_type_db)
    session.commit()
    session.refresh(pass_type_db)
    return pass_type_db
