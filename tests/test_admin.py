import pytest
import sys
import os
import uuid
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Agrega el path raíz del proyecto
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
    """Inserta directamente el admin raíz si no existe"""
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
        print("✅ Admin raíz insertado directamente en la base de datos")

def test_admin_lifecycle(client):
    """Crea un admin raíz si no existe, luego crea, accede y elimina un nuevo admin"""

    # Paso 1: asegurar que el admin raíz exista
    ensure_root_admin_exists()

    # Paso 2: login con admin raíz
    root_login = client.post("/api/auth/login", json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })

    print("Login root admin:", root_login.status_code, root_login.get_json())
    assert root_login.status_code == 200
    root_token = root_login.get_json()["data"]["access_token"]

    # Paso 3: crear nuevo admin
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = "Test1234"

    create_resp = client.post("/api/admins/", json={
        "username": username,
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "User"
    }, headers={"Authorization": f"Bearer {root_token}"})

    print("Crear admin:", create_resp.status_code, create_resp.get_json())
    assert create_resp.status_code in [200, 201]

    # Paso 4: login con el nuevo admin
    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    print("Login nuevo admin:", login_resp.status_code, login_resp.get_json())
    assert login_resp.status_code == 200

    login_data = login_resp.get_json()["data"]
    new_token = login_data["access_token"]
    new_admin_id = login_data["admin"]["_id"]

    # Paso 5: acceder a endpoint protegido
    protected = client.get("/api/admins/", headers={
        "Authorization": f"Bearer {new_token}"
    })
    print("Acceso protegido:", protected.status_code)
    assert protected.status_code == 200

    # Paso 6: eliminar admin
    delete = client.delete(f"/api/admins/{new_admin_id}", headers={
        "Authorization": f"Bearer {root_token}"
    })
    print("Eliminar admin:", delete.status_code, delete.get_json())
    assert delete.status_code in [200, 204]
