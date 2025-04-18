def auth_headers(client):
    client.post("/users/register", json={
        "username": "writer",
        "email": "writer@example.com",
        "password": "secret"
    })
    res = client.post("/users/login", json={
        "email": "writer@example.com",
        "password": "secret"
    })
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_post(client):
    headers = auth_headers(client)
    res = client.post("/community/", json={
        "title": "Panduan Kompos",
        "content": "Cara membuat kompos dari sampah rumah tangga",
        "type": "article"
    }, headers=headers)
    assert res.status_code == 201
    assert b"Post created" in res.data

def test_get_posts(client):
    res = client.get("/community/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
