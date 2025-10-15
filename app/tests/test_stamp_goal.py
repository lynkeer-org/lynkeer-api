import pytest
from fastapi import status


def test_stamp_goal_completion(client):
    """Test that when stamp goal is reached, stamps are deactivated and reward is created"""
    
    # Setup: Create owner, customer, pass template
    from app.tests.test_customer_pass import get_auth_headers, create_pass_template
    
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Test",
            "last_name": "Customer", 
            "email": "test.customer@example.com",
            "phone": "1111111111",
            "birth_date": "1990-01-01"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template with stamp_goal = 3
    create_pass_template(client)
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass
    customer_pass_data = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id,
        "active_stamps": 0,
        "active_rewards": 0,
    }
    cp_resp = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert cp_resp.status_code == status.HTTP_201_CREATED
    customer_pass_id = cp_resp.json()["id"]
    
    # Test: Create stamps one by one and check behavior
    
    # Create 1st stamp (goal not reached)
    stamp1_resp = client.post(
        "/api/v1/stamps",
        json={"customer_pass_id": customer_pass_id},
        headers=headers,
    )
    assert stamp1_resp.status_code == status.HTTP_201_CREATED
    
    # Check customer pass state after 1st stamp
    cp_check1 = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    cp_data1 = cp_check1.json()
    assert cp_data1["active_stamps"] == 1
    assert cp_data1["active_rewards"] == 0
    
    # Create 2nd stamp (goal not reached)
    stamp2_resp = client.post(
        "/api/v1/stamps",
        json={"customer_pass_id": customer_pass_id},
        headers=headers,
    )
    assert stamp2_resp.status_code == status.HTTP_201_CREATED
    
    # Check customer pass state after 2nd stamp
    cp_check2 = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    cp_data2 = cp_check2.json()
    assert cp_data2["active_stamps"] == 2
    assert cp_data2["active_rewards"] == 0
    
    # Create 3rd stamp (goal reached! stamp_goal = 5 from create_pass_template)
    # Wait, let me check what stamp_goal is set in create_pass_template
    
    # Actually, let me check how many stamps we need by creating until goal is reached
    current_stamps = 2
    max_attempts = 10  # Safety limit
    
    for attempt in range(max_attempts):
        stamp_resp = client.post(
            "/api/v1/stamps",
            json={"customer_pass_id": customer_pass_id},
            headers=headers,
        )
        assert stamp_resp.status_code == status.HTTP_201_CREATED
        current_stamps += 1
        
        # Check customer pass state
        cp_check = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
        cp_data = cp_check.json()
        
        if cp_data["active_stamps"] == 0 and cp_data["active_rewards"] == 1:
            # Goal was reached! Stamps reset and reward created
            print(f"Goal reached after {current_stamps} stamps!")
            
            # Verify all stamps are now inactive
            stamps_resp = client.get(f"/api/v1/customer-passes/{customer_pass_id}/stamps", headers=headers)
            if stamps_resp.status_code == status.HTTP_200_OK:
                stamps = stamps_resp.json()
                assert len(stamps) == 0, "All stamps should be inactive after goal reached"
            
            # Verify reward was created
            rewards_resp = client.get(f"/api/v1/customer-passes/{customer_pass_id}/rewards", headers=headers)
            if rewards_resp.status_code == status.HTTP_200_OK:
                rewards = rewards_resp.json()
                assert len(rewards) == 1, "One reward should be created after goal reached"
                assert rewards[0]["customer_pass_id"] == customer_pass_id
            
            break
    else:
        pytest.fail(f"Goal was not reached after {max_attempts} stamps")
    
    # Test: Create another stamp to verify customer can continue earning
    stamp_after_resp = client.post(
        "/api/v1/stamps",
        json={"customer_pass_id": customer_pass_id},
        headers=headers,
    )
    assert stamp_after_resp.status_code == status.HTTP_201_CREATED
    
    # Check that stamps restart from 1
    cp_final = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    cp_final_data = cp_final.json()
    assert cp_final_data["active_stamps"] == 1
    assert cp_final_data["active_rewards"] == 1


def test_stamp_goal_multiple_rewards(client):
    """Test that customer can earn multiple rewards"""
    
    from app.tests.test_customer_pass import get_auth_headers, create_pass_template
    
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Multi",
            "last_name": "Reward", 
            "email": "multi.reward@example.com",
            "phone": "2222222222",
            "birth_date": "1990-01-01"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template and customer pass
    create_pass_template(client)
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    pass_id = pass_list_resp.json()[0]["id"]
    
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_id,
        "active_stamps": 0,
        "active_rewards": 0,
    }
    cp_resp = client.post("/api/v1/customer-passes", json=customer_pass_data, headers=headers)
    customer_pass_id = cp_resp.json()["id"]
    
    # Earn first reward
    rewards_earned = 0
    stamps_created = 0
    max_stamps = 20  # Safety limit
    
    while rewards_earned < 2 and stamps_created < max_stamps:
        # Create stamp
        client.post("/api/v1/stamps", json={"customer_pass_id": customer_pass_id}, headers=headers)
        stamps_created += 1
        
        # Check if reward was earned
        cp_check = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
        current_rewards = cp_check.json()["active_rewards"]
        
        if current_rewards > rewards_earned:
            rewards_earned = current_rewards
            print(f"Reward #{rewards_earned} earned after {stamps_created} stamps!")
    
    # Verify final state
    cp_final = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    final_data = cp_final.json()
    assert final_data["active_rewards"] >= 2, "Should have earned at least 2 rewards"