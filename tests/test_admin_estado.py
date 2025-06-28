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
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_admin_desactivado_no_puede_loguearse(client):
    """Un admin desactivado no puede iniciar sesión"""

    email = f"disabled_{uuid.uuid4().hex[:6]}@example.com"
    password = "Test1234"

    # Insertar directamente en la base un admin desactivado
    db_client = MongoClient(MONGO_URI)
    db = db_client.get_database('test_admin_db')

    db.admins.insert_one({
        "username": f"user_{uuid.uuid4().hex[:6]}",
        "email": email,
        "password": generate_password_hash(password),
        "first_name": "Inactivo",
        "last_name": "Admin",
        "role": "admin",
        "is_active": False
    })

    # Intentar login
    resp = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    print("Login admin desactivado:", resp.status_code, resp.get_json())
    assert resp.status_code == 401
    assert "desactivada" in resp.get_json()["message"].lower() or "credenciales" in resp.get_json()["message"].lower()
