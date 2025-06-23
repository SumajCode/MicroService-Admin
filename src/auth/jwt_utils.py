from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import timedelta
import secrets

def generate_tokens(admin_data):
    """Generar access y refresh tokens"""
    try:
        # Datos adicionales para el token
        additional_claims = {
            "username": admin_data.get('username'),
            "role": admin_data.get('role', 'admin'),
            "email": admin_data.get('email')
        }
        
        access_token = create_access_token(
            identity=str(admin_data['_id']),
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        refresh_token = create_refresh_token(
            identity=str(admin_data['_id']),
            expires_delta=timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
    except Exception as e:
        print(f"Error generando tokens: {e}")
        return None

def generate_secure_token():
    """Generar token seguro para refresh"""
    return secrets.token_urlsafe(32)

def get_current_admin_id():
    """Obtener ID del admin actual desde el JWT"""
    try:
        return get_jwt_identity()
    except Exception as e:
        print(f"Error obteniendo admin ID: {e}")
        return None

def get_token_claims():
    """Obtener claims del token actual"""
    try:
        return get_jwt()
    except Exception as e:
        print(f"Error obteniendo claims: {e}")
        return None
