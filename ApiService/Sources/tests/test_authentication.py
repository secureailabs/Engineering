from datetime import datetime
from time import sleep
import pytest
import unittest
from pydantic import EmailStr
from models.datasets import RegisterDataset_In
from models.users import User_In
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient
from app.main import server


class Major(unittest.TestCase):
    dataOwnerToken = ''
    researcherToken = ''
    test_app = TestClient(server)

    def test_a_register_dataowner(self):
        user = User_In(username="johndoe", email=EmailStr('user@example.com'), phone="string", password="secret")
        response = self.test_app.post("/user", json=jsonable_encoder(user))
        assert response.status_code == 200

    def test_b_register_researcher(self):
        user = User_In(username="foobar", email=EmailStr('user@example.com'), phone="string", password="secret")
        response = self.test_app.post("/user", json=jsonable_encoder(user))
        assert response.status_code == 200

    def test_c_login_dataowner(self):
        login = {"grant_type": "", "username": "johndoe", "password": "secret", "scope": "", "client_id": "", "client_secret": ""}
        response = self.test_app.post("/token", data=login)
        self.dataOwnerToken = response.json()["access_token"]
        assert response.status_code == 200

    def test_d_login_researcher(self):
        login = {"grant_type": "", "username": "foobar", "password": "secret", "scope": "", "client_id": "", "client_secret": ""}
        response = self.test_app.post("/token", data=login)
        self.researcherToken = response.json()["access_token"]
        assert response.status_code == 200

    def test_e_register_dataset(self):
        dataset = RegisterDataset_In(Name="test", Description="test", Version="5e9f8f8f8f8f8f8f8f8f8f8", Keywords="5e9f8f8f8f8f8f8f8f8f8f8", PublishDate=datetime.utcnow(), JurisdictionalLimitations="sd")
        header = {"Authentication": "Bearer " + self.dataOwnerToken}
        response = self.test_app.post("/dataset", json=jsonable_encoder(dataset), headers=header)
        assert response.status_code == 200

# def test_register_organization(self, test_app):
#     response = test_app.get("/register")
#     assert response.status_code == 200
#     assert response.json() == {"ping": "pong!"}
