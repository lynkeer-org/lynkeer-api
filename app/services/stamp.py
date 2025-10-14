from fastapi import HTTPException, status
from app.crud.stamp import (
    create_stamp,
    delete_stamp,    
    read_stamp,
    count_active_stamps_by_customer_pass_id,
    deactivate_all_stamps_by_customer_pass_id,
)
from app.crud.customer_pass import read_customer_pass, update_customer_pass
from app.crud.pass_model import read_pass
from app.crud.reward import create_reward
from app.models.stamp import Stamp
from app.models.reward import Reward
from app.schemas.stamp import StampCreate
from app.schemas.customer_pass import CustomerPassUpdate
from app.core.db import SessionDep
import uuid


def create_stamp_service(stamp_data: StampCreate, session: SessionDep, owner_id: uuid.UUID | None = None):
    stamp_data_dict = stamp_data.model_dump()
    customer_pass_id_raw = stamp_data_dict.get("customer_pass_id")
    
    if not customer_pass_id_raw:
        raise HTTPException(status_code=400, detail="customer_pass_id is required")

    try:
        customer_pass_id: uuid.UUID = customer_pass_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for customer_pass_id")

    # Validate that the customer_pass exists and is active
    customer_pass = read_customer_pass(
        customer_pass_id=customer_pass_id, session=session
    )
    if not customer_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CustomerPass does not exist"
        )
    if not customer_pass.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CustomerPass is not active"
        )

    
    # Owner validation: validate ownership through pass template    
    pass_model = read_pass(customer_pass.pass_id, session)
    if pass_model.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only create stamps for customer passes from your own pass templates"
        )    
        

    # Create the new stamp first
    stamp = Stamp.model_validate(stamp_data_dict)
    created_stamp = create_stamp(stamp, session)

    # Business Logic: Check if stamp goal is reached
    
    # Count active stamps after creating the new one
    active_stamp_count = count_active_stamps_by_customer_pass_id(customer_pass_id, session)
    
    if active_stamp_count >= pass_model.stamp_goal:
        # Goal reached! Reset stamps and create reward
        
        # 1. Deactivate all stamps for this customer_pass
        deactivate_all_stamps_by_customer_pass_id(customer_pass_id, session)
        
        # 2. Create a new reward
        reward = Reward(customer_pass_id=customer_pass_id)
        created_reward = create_reward(reward, session)
        
        # 3. Update customer_pass counts: reset active_stamps=0, increment active_rewards
        update_data = CustomerPassUpdate(
            active_stamps=0,
            active_rewards=customer_pass.active_rewards + 1
        )
        update_customer_pass(customer_pass, update_data, session)
        
    else:
        # Goal not reached, just update active_stamps count
        update_data = CustomerPassUpdate(active_stamps=active_stamp_count)
        update_customer_pass(customer_pass, update_data, session)

    return created_stamp



def delete_stamp_service(stamp_id: uuid.UUID, session: SessionDep):
    stamp_db = read_stamp(stamp_id=stamp_id, session=session)
    if not stamp_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The stamp does not exist",
        )

    return delete_stamp(stamp_db, session)
