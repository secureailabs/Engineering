from starlette.testclient import TestClient
from pydantic import EmailStr
from app.main import server
from models.accounts import RegisterOrganization_In, RegisterOrganization_Out
from fastapi.encoders import jsonable_encoder

client = TestClient(app=server, base_url="http://127.0.0.1:8000")


def test_register_dataowner():
    user = RegisterOrganization_In(
        name="KCA",
        description="test",
        adminName="John Doe",
        adminJobTitle="test",
        adminEmail=EmailStr("johndoe2@kca.com"),
        adminPassword="secret",
    )
    response = client.post("/organizations", json=jsonable_encoder(user))
    assert response.status_code == 201
    assert RegisterOrganization_Out(**response.json()) is not None


def test_register_dataowner_again():
    user = RegisterOrganization_In(
        name="KCA",
        description="test",
        adminName="John Doe",
        adminJobTitle="test",
        adminEmail=EmailStr("johndoe2@kca.com"),
        adminPassword="secret",
    )
    response = client.post("/organizations", json=jsonable_encoder(user))
    assert response.status_code == 409


def test_register_register():
    user = RegisterOrganization_In(
        name="MGH",
        description="test",
        adminName="Mufasa",
        adminJobTitle="King",
        adminEmail=EmailStr("mufasa@hakuna.com"),
        adminPassword="secret",
    )
    response = client.post("/organizations", json=jsonable_encoder(user))
    assert response.status_code == 201
    assert RegisterOrganization_Out(**response.json()) is not None
