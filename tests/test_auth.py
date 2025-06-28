import pytest
import sys
import os
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

def test_login_existing_admin(client):
    """Asegura que el admin exista y verifica que puede loguearse correctamente"""

    ensure_root_admin_exists()

    response = client.post('/api/auth/login', json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })

    print("Login response:", response.status_code, response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert data.get("success") is True
    assert "access_token" in data["data"]

def test_refresh_token_valido(client):
    """Renueva el access_token usando un refresh_token válido"""

    ensure_root_admin_exists()

    login = client.post('/api/auth/login', json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })
    assert login.status_code == 200
    tokens = login.get_json()["data"]
    refresh_token = tokens["refresh_token"]

    resp = client.post('/api/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    print("Refresh response:", resp.status_code, resp.get_json())
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()["data"]

def test_logout_revoca_sesion(client):
    """Logout revoca la sesión y el refresh_token ya no es válido"""

    ensure_root_admin_exists()

    login = client.post('/api/auth/login', json={
        "email": "kevinurena82@gmail.com",
        "password": "123456789"
    })
    assert login.status_code == 200
    tokens = login.get_json()["data"]
    refresh_token = tokens["refresh_token"]

    logout = client.post('/api/auth/logout', json={
        "refresh_token": refresh_token
    }, headers={"Authorization": f"Bearer {tokens['access_token']}"})
    print("Logout:", logout.status_code, logout.get_json())
    assert logout.status_code == 200

    refresh = client.post('/api/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    print("Refresh post-logout:", refresh.status_code, refresh.get_json())
    assert refresh.status_code == 401
def test_login_email_inexistente(client):
    """Debe fallar el login si el email no está registrado"""

    response = client.post('/api/auth/login', json={
        "email": "inexistente999@example.com",
        "password": "cualquierclave"
    })

    print("Login con email inexistente:", response.status_code, response.get_json())
    assert response.status_code == 401
    assert response.get_json().get("message") == "Credenciales inválidas"

def test_login_contraseña_incorrecta(client):
    """Debe fallar si el email existe pero la contraseña es incorrecta"""

    ensure_root_admin_exists()

    response = client.post('/api/auth/login', json={
        "email": "kevinurena82@gmail.com",
        "password": "clave_incorrecta"
    })

    print("Login con contraseña incorrecta:", response.status_code, response.get_json())
    assert response.status_code == 401
    assert response.get_json().get("message") == "Credenciales inválidas"
