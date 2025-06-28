import pytest
import sys
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Setup imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import create_app

MONGO_URI = 'mongodb+srv://kevinurena82:kW8x5NlzPioQsqJf@cluster0.ftrgo1z.mongodb.net/test_admin_db?retryWrites=true&w=majority'

@pytest.fixture
def app():
    os.environ['MONGO_URI'] = MONGO_URI
    os.environ['JWT_SECRET_KEY'] = 'supersecretkey'
    os.environ['SECRET_KEY'] = 'supersecretkey'
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def ensure_root_admin_exists():
    client = MongoClient(MONGO_URI)
    db = client.get_database('test_admin_db')
    if not db.admins.find_one({"email": "kevinurena82@gmail.com"}):
        db.admins.insert_one({
            "username": "adminroot",
            "email": "kevinurena82@gmail.com",
            "password": generate_password_hash("123456789"),
            "first_name": "Admin",
            "last_name": "Root",
            "role": "admin",
            "is_active": True
        })

def login_root(client):
    ensure_root_admin_exists()
    response = client.post("/api/auth/login", json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })
    return response.get_json()["data"]["access_token"]

# =============================
# Tests simples y directos
# =============================

def test_login_con_json_vacio(client):
    resp = client.post("/api/auth/login", json={})
    assert resp.status_code == 400

def test_login_sin_email(client):
    resp = client.post("/api/auth/login", json={"password": "algo"})
    assert resp.status_code == 400

def test_login_sin_password(client):
    resp = client.post("/api/auth/login", json={"email": "algo@example.com"})
    assert resp.status_code == 400

def test_get_admins_con_token(client):
    token = login_root(client)
    resp = client.get("/api/admins/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_get_admins_sin_token(client):
    resp = client.get("/api/admins/")
    assert resp.status_code == 401

def test_get_admins_token_falso(client):
    resp = client.get("/api/admins/", headers={"Authorization": "Bearer falso.token"})
    assert resp.status_code in [401, 422]

def test_me_endpoint_funciona(client):
    token = login_root(client)
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_me_endpoint_sin_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401

def test_logout_sin_refresh_token(client):
    token = login_root(client)
    resp = client.post("/api/auth/logout", json={}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200  # El logout sin refresh_token igual debería responder OK
