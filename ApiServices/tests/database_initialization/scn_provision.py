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
# base_url = "https://public_ip:8000" # Use this for non docker deployments
researcher_email = "admin@secureailabs.com"
sail_password = "SailPassword@123"

# encode email and password to url
researcher_email = researcher_email.replace("@", "%40")
sail_password = sail_password.replace("@", "%40")

# Data researcher login
payload = f"grant_type=&username={researcher_email}&password={sail_password}&scope=&client_id=&client_secret="
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(f"{base_url}/login", data=payload, headers=headers, verify=False)
data_federation_researcher_token = response.json().get("access_token")

# Data researcher gets the data federation
headers = {"Authorization": f"Bearer {data_federation_researcher_token}"}
response = requests.get(
    f"{base_url}/data-federations",
    headers=headers,
    verify=False,
)
data_federation_id = response.json().get("data_federations")[0].get("id")

# Data researcher create data federation provision
payload = {"data_federation_id": data_federation_id, "secure_computation_nodes_type": "Standard_D4s_v4"}
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {data_federation_researcher_token}"}
response = requests.post(
    f"{base_url}/data-federations-provisions",
    json=payload,
    headers=headers,
    verify=False,
)
data_federation_provision_id = response.json().get("id")
print(data_federation_provision_id)


# Deporvision data federation
headers = {"Authorization": f"Bearer {data_federation_researcher_token}"}
response = requests.delete(
    f"{base_url}/data-federations-provisions/{data_federation_provision_id}",
    headers=headers,
    verify=False,
)
assert response.status_code == 204
