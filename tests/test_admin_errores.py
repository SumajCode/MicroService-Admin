import pytest
import sys
import os
import uuid
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

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
# Tests negativos de /api/admins/
# =============================

def test_crear_admin_sin_email(client):
    token = login_root(client)
    resp = client.post("/api/admins/", json={
        "username": "noemail",
        "password": "Test1234"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400

def test_crear_admin_sin_password(client):
    token = login_root(client)
    resp = client.post("/api/admins/", json={
        "username": "nopass",
        "email": f"np_{uuid.uuid4().hex[:6]}@example.com"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400

def test_crear_admin_email_duplicado(client):
    token = login_root(client)

    email = f"dup_{uuid.uuid4().hex[:6]}@example.com"

    # Crear admin una vez
    first = client.post("/api/admins/", json={
        "username": f"user_{uuid.uuid4().hex[:6]}",
        "email": email,
        "password": "Test1234"
    }, headers={"Authorization": f"Bearer {token}"})
    assert first.status_code in [200, 201]

    # Intentar crear otro con el mismo email
    second = client.post("/api/admins/", json={
        "username": f"user_{uuid.uuid4().hex[:6]}",
        "email": email,
        "password": "Test1234"
    }, headers={"Authorization": f"Bearer {token}"})
    assert second.status_code == 400

def test_actualizar_admin_inexistente(client):
    token = login_root(client)
    fake_id = "000000000000000000000000"  # ID de Mongo válido pero no existente
    resp = client.put(f"/api/admins/{fake_id}", json={
        "first_name": "Nada"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code in [400, 404]

def test_eliminar_admin_inexistente(client):
    token = login_root(client)
    fake_id = "000000000000000000000000"
    resp = client.delete(f"/api/admins/{fake_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in [400, 404, 204]
