import json

def auth_headers(client):
    client.post("/users/register", json={
        "username": "seller",
        "email": "seller@example.com",
        "password": "secret123"
    })
    res = client.post("/users/login", json={
        "email": "seller@example.com",
        "password": "secret123"
    })
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_product(client):
    headers = auth_headers(client)
    res = client.post("/products/", json={
        "name": "Sabun Batang",
        "description": "Sabun natural tanpa kemasan",
        "price": 15000,
        "stock": 10
    }, headers=headers)
    assert res.status_code == 201
    assert b"Product created" in res.data

def test_get_products(client):
    res = client.get("/products/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
