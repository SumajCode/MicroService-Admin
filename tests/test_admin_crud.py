import pytest
import sys
import os
import uuid
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Setup import path
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
    """Crea el admin raíz directamente si no existe"""
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

def test_admin_crud(client):
    """Prueba básica: crear, listar y eliminar un admin"""

    ensure_root_admin_exists()

    # Login admin raíz
    login = client.post("/api/auth/login", json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]

    # Crear nuevo admin
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = "Test1234"

    create = client.post("/api/admins/", json={
        "username": username,
        "email": email,
        "password": password,
        "first_name": "Nuevo",
        "last_name": "Admin"
    }, headers={"Authorization": f"Bearer {token}"})
    assert create.status_code in [200, 201]

    # Obtener lista de admins
    list_resp = client.get("/api/admins/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert list_resp.status_code == 200
    admins = list_resp.get_json()["data"]["admins"]

    # Buscar el nuevo admin en la lista
    admin_id = next((a["_id"] for a in admins if a["email"] == email), None)
    assert admin_id is not None

    # Eliminar el nuevo admin
    delete_resp = client.delete(f"/api/admins/{admin_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert delete_resp.status_code in [200, 204]
