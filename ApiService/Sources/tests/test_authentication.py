def test_login(test_app):
    response = test_app.get("/login")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_register_user(test_app):
    response = test_app.get("/register")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_register_organization(test_app):
    response = test_app.get("/register")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
