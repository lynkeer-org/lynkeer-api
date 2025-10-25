import pytest
from fastapi import status

from app.tests.test_customer_pass import get_auth_headers, create_pass_template

def test_claim_rewards_endpoint(client):
	"""Test claiming rewards via the claim_rewards endpoint"""
	headers = get_auth_headers(client)

	# Create a customer
	customer_resp = client.post(
		"/api/v1/customers",
		json={
			"first_name": "Claim",
			"last_name": "Test",
			"email": "claim.test@example.com",
			"phone": "3333333333",
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
	assert cp_resp.status_code == status.HTTP_201_CREATED
	customer_pass_id = cp_resp.json()["id"]

	# Earn two rewards by creating enough stamps (simulate earning, not claiming)
	rewards_earned = 0
	max_stamps = 20
	while rewards_earned < 2 and max_stamps > 0:
		stamp_resp = client.post("/api/v1/stamps", json={"customer_pass_id": customer_pass_id}, headers=headers)
		assert stamp_resp.status_code == status.HTTP_201_CREATED
		rewards_earned = stamp_resp.json()["active_rewards"]
		max_stamps -= 1
	assert rewards_earned >= 2, "Should have earned at least 2 rewards before claiming"

	# List rewards before claiming
	rewards_resp = client.get(f"/api/v1/customer-passes/{customer_pass_id}/rewards", headers=headers)
	assert rewards_resp.status_code == status.HTTP_200_OK
	rewards = rewards_resp.json()
	# All rewards should be active and unclaimed
	active_rewards = [r for r in rewards if r["active"]]
	assert len(active_rewards) >= 2
	assert all(r["claimed_at"] is None for r in active_rewards)

	# Save the ids and issued_at of the rewards before claiming
	reward_ids_before = [r["id"] for r in active_rewards]
	issued_ats_before = [r["issued_at"] for r in active_rewards]

	# Claim 1 reward (should claim the oldest by issued_at)
	claim_resp = client.get(
		f"/api/v1/rewards/claim-reward/{customer_pass_id}",
		params={"number_of_rewards": 1},
		headers=headers,
	)
	assert claim_resp.status_code == status.HTTP_200_OK
	cp_after_claim = claim_resp.json()
	# active_rewards should be decremented by 1
	assert cp_after_claim["active_rewards"] == rewards_earned - 1

	# List rewards after claiming
	rewards_after_resp = client.get(f"/api/v1/customer-passes/{customer_pass_id}/rewards", headers=headers)
	assert rewards_after_resp.status_code == status.HTTP_200_OK
	rewards_after = rewards_after_resp.json()

	# There should be exactly one claimed reward
	claimed = [r for r in rewards_after if r["claimed_at"] is not None]
	assert len(claimed) == 1
	assert claimed[0]["active"] is False

	# The claimed reward should be the one with the oldest issued_at
	oldest_issued_at = min(issued_ats_before)
	claimed_issued_at = claimed[0]["issued_at"]
	assert claimed_issued_at == oldest_issued_at

	# The rest should still be unclaimed and active
	unclaimed = [r for r in rewards_after if r["claimed_at"] is None and r["active"]]
	assert len(unclaimed) == rewards_earned - 1
	# Their ids should be a subset of the original reward ids
	unclaimed_ids = set(r["id"] for r in unclaimed)
	assert unclaimed_ids.issubset(set(reward_ids_before))
