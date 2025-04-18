def test_register_user(client):
    res = client.post("/users/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "secret123"
    })
    assert res.status_code == 201
    assert b"User registered successfully" in res.data

def test_login_user(client):
    client.post("/users/register", json={
        "username": "tester2",
        "email": "tester2@example.com",
        "password": "secret123"
    })
    res = client.post("/users/login", json={
        "email": "tester2@example.com",
        "password": "secret123"
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()
