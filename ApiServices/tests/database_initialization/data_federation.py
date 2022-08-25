# -------------------------------------------------------------------------------
# Engineering
# data_federation.py
# -------------------------------------------------------------------------------
"""Initialize database with data federation information"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.

import requests

#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

base_url = "http://127.0.0.1:8000"

# Federation owner login
payload = f"grant_type=&username=sallie%40kidneycancer.org&password=SailPassword%40123&scope=&client_id=&client_secret="
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(f"{base_url}/login", data=payload, headers=headers, verify=False)
data_federation_owner_token = response.json().get("access_token")

# Data submitter login
payload = f"grant_type=&username=nadams%40mghl.com&password=SailPassword%40123&scope=&client_id=&client_secret="
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(f"{base_url}/login", data=payload, headers=headers, verify=False)
data_federation_data_submitter_token = response.json().get("access_token")

# Data submitter org id
headers = {"Authorization": f"Bearer {data_federation_data_submitter_token}"}
response = requests.get(f"{base_url}/me", headers=headers, verify=False)
data_federation_data_submitter_org_id = response.json().get("organization").get("id")

# Data researcher login
payload = f"grant_type=&username=lbart%40igr.com&password=SailPassword%40123&scope=&client_id=&client_secret="
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(f"{base_url}/login", data=payload, headers=headers, verify=False)
data_federation_researcher_token = response.json().get("access_token")

# Create data federation
payload = {"name": "Cancer Federation", "description": "federation to enable cancer research"}
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {data_federation_owner_token}"}
response = requests.post(f"{base_url}/data-federations", json=payload, headers=headers, verify=False)
data_federation_id = response.json().get("id")

# Invite data submitter to data federation
headers = {"Authorization": f"Bearer {data_federation_owner_token}"}
response = requests.put(
    f"{base_url}/data-federations/{data_federation_id}/data-submitter/{data_federation_data_submitter_org_id}",
    headers=headers,
    verify=False,
)
assert response.status_code == 204

# Data submitter lists data federation invitation
headers = {"Authorization": f"Bearer {data_federation_data_submitter_token}"}
response = requests.get(
    f"{base_url}/data-federations/{data_federation_data_submitter_org_id}/invites", headers=headers, verify=False
)
federation_invite_id = response.json().get("invites")[0].get("id")

# Data submitter accept data federation invitation
payload = {"state": "ACCEPTED"}
headers = {"Authorization": f"Bearer {data_federation_data_submitter_token}"}
response = requests.patch(
    f"{base_url}/data-federations/{data_federation_data_submitter_org_id}/invites/{federation_invite_id}",
    json=payload,
    headers=headers,
    verify=False,
)
assert response.status_code == 204


# Data submitter gets the list of all datasets
headers = {"Authorization": f"Bearer {data_federation_data_submitter_token}"}
response = requests.get(f"{base_url}/datasets", headers=headers, verify=False)
dataset_id = response.json().get("datasets")[0].get("id")


# Data submitter adds dataset to data federation
headers = {"Authorization": f"Bearer {data_federation_data_submitter_token}"}
response = requests.put(
    f"{base_url}/data-federations/{data_federation_id}/datasets/{dataset_id}",
    headers=headers,
    verify=False,
)
assert response.status_code == 204


# Data federation owner deletes the dataset from data federation
# headers = {"Authorization": f"Bearer {data_federation_owner_token}"}
# response = requests.delete(
#     f"{base_url}/data-federations/{data_federation_id}/datasets/{dataset_id}",
#     headers=headers,
#     verify=False,
# )
# assert response.status_code == 204
