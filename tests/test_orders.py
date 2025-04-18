def setup_product_and_token(client):
    # Register & login user
    client.post("/users/register", json={
        "username": "buyer",
        "email": "buyer@example.com",
        "password": "secret"
    })
    login = client.post("/users/login", json={
        "email": "buyer@example.com",
        "password": "secret"
    })
    token = login.get_json()["access_token"]

    # Add product
    client.post("/products/", json={
        "name": "Sikat Bambu",
        "description": "Sikat dari bambu ramah lingkungan",
        "price": 20000,
        "stock": 5
    }, headers={"Authorization": f"Bearer {token}"})

    return token

def test_create_order(client):
    token = setup_product_and_token(client)

    # Get product ID
    products = client.get("/products/").get_json()
    product_id = products[0]["id"]

    res = client.post("/orders/", json={
        "product_id": product_id,
        "quantity": 2
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 201
    assert b"Order placed successfully" in res.data

def test_get_user_orders(client):
    token = setup_product_and_token(client)

    res = client.get("/orders/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
