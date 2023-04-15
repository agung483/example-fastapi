import pytest
from app import schemas
#from .database import client, session
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Welcome to my Api'
    assert res.status_code == 200

#pytest membedakan antara /users/ dengan /users, shg sebaiknya selalu gunakan sesuai dengan yg didefinisikan di routers .
def test_create_user(client):
    res = client.post("/users/", json={"username": "totok","email": "totok@gmail.com", "password": "password12"})
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "totok@gmail.com"
    assert res.status_code == 201    

# disini pakai /login, karena di auth.py (folder routers) dideclarasikan /login
# dibutuhkan disimpan dalam form data, jadi instead of pakai json diganti dengan data.
def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
                        ('Joni', 'password12', 403),
                        ('totok', 'passwordSalah', 403),
                        ('budi', 'passwordSalah', 403),
                        (None, 'password12', 422),
                        ('totok', None, 422)    
                         ])
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Credentials"
