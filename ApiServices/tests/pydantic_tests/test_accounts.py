from app.main import server
from fastapi.encoders import jsonable_encoder
from models.accounts import RegisterOrganization_In, RegisterOrganization_Out
from pydantic import EmailStr
from starlette.testclient import TestClient

client = TestClient(app=server, base_url="https://127.0.0.1:8000")


def test_register_org_dataowner():
    """
    Register Organization
    """
    user = RegisterOrganization_In(
        name="KCA",
        description="test",
        admin_name="John Doe",
        admin_job_title="test",
        admin_email=EmailStr("johndoe4@kca.com"),
        admin_password="secret",
    )
    response = client.post("/organizations", json=jsonable_encoder(user))
    assert response.status_code == 201
    assert RegisterOrganization_Out(**response.json()) is not None


def test_get_organizations():
    """
    Get List of Organizations
    """
    # user = RegisterOrganization_In(
    #     name="KCA",
    #     description="test",
    #     admin_name="John Doe",
    #     admin_job_title="test",
    #     admin_email=EmailStr("johndoe4@kca.com"),
    #     admin_password="secret",
    # )
    client = TestClient(app=server, base_url="https://127.0.0.1:8000")
    payload = f"username=johndoe4@kca.com&password=secret"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    login_response = client.post("/login", headers=headers, data=payload, verify=False)
    authed_user_access_token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {authed_user_access_token}", "Accept": "application/json"}
    # headers = {"Accept": "application/json", "Authorization": f"Bearer {authed_user_access_token}"}
    authorization_response = client.get("/me", headers=headers, verify=False)
    response = client.get("/organizations")
    assert response.status_code == 200
    # assert RegisterOrganization_Out(**response.json()) is not None


# def test_register_dataowner_again():
#     user = RegisterOrganization_In(
#         name="KCA",
#         description="test",
#         admin_name="John Doe",
#         admin_job_title="test",
#         admin_email=EmailStr("johndoe2@kca.com"),
#         admin_password="secret",
#     )
#     response = client.post("/organizations", json=jsonable_encoder(user))
#     assert response.status_code == 409


# def test_register_register():
#     user = RegisterOrganization_In(
#         name="MGH",
#         description="test",
#         admin_name="Mufasa",
#         admin_job_title="King",
#         admin_email=EmailStr("mufasa@hakuna.com"),
#         admin_password="secret",
#     )
#     response = client.post("/organizations", json=jsonable_encoder(user))
#     assert response.status_code == 201
#     assert RegisterOrganization_Out(**response.json()) is not None
