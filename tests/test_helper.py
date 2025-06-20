import pytest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.app import create_app

@pytest.fixture
def app():
    """Crear aplicación para pruebas"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_admin_db'
    return app

@pytest.fixture
def client(app):
    """Cliente de pruebas"""
    return app.test_client()

def test_helper_endpoint_success(client):
    """Test exitoso del endpoint /helper"""
    response = client.get('/api/helper')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == "Helper endpoint funcionando"
    assert 'data' in data
    assert data['data']['version'] == "1.0.0"
    assert data['data']['service'] == "admin-microservice"

def test_helper_endpoint_method_not_allowed(client):
    """Test con método no permitido (POST en lugar de GET)"""
    response = client.post('/api/helper')
    
    assert response.status_code == 405  # Method Not Allowed

def test_health_endpoint_success(client):
    """Test del endpoint de salud"""
    response = client.get('/api/health')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == "Servidor funcionando correctamente"
    assert data['data']['status'] == "healthy"

def test_nonexistent_endpoint(client):
    """Test de endpoint inexistente"""
    response = client.get('/api/nonexistent')
    
    assert response.status_code == 404

def test_helper_response_structure(client):
    """Test de estructura de respuesta del helper"""
    response = client.get('/api/helper')
    data = response.get_json()
    
    # Verificar estructura de respuesta
    required_keys = ['success', 'message', 'data']
    for key in required_keys:
        assert key in data
    
    # Verificar tipos de datos
    assert isinstance(data['success'], bool)
    assert isinstance(data['message'], str)
    assert isinstance(data['data'], dict)
    
    # Verificar contenido de data
    assert 'version' in data['data']
    assert 'service' in data['data']
