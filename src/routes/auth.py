from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.admin import AdminModel
from src.services.session import SessionService
from src.auth.jwt_utils import generate_tokens

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Email y contraseña son requeridos",
                "data": None
            }), 400
        
        admin_model = AdminModel(current_app.db)
        session_service = SessionService(current_app.db)
        
        # Verificar credenciales
        admin = admin_model.verify_password(data['email'], data['password'])
        
        if not admin:
            return jsonify({
                "success": False,
                "message": "Credenciales inválidas",
                "data": None
            }), 401
        
        if not admin.get('is_active', True):
            return jsonify({
                "success": False,
                "message": "Cuenta desactivada",
                "data": None
            }), 401
        
        # Generar tokens
        tokens = generate_tokens(admin)
        if not tokens:
            return jsonify({
                "success": False,
                "message": "Error generando tokens",
                "data": None
            }), 500
        
        # Crear sesión
        session_data, session_message = session_service.create_session(
            admin_id=str(admin['_id']),
            refresh_token=tokens['refresh_token']
        )
        
        return jsonify({
            "success": True,
            "message": "Login exitoso",
            "data": {
                "admin": admin,
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en login: {str(e)}",
            "data": None
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar access token"""
    try:
        current_admin_id = get_jwt_identity()
        refresh_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        admin_model = AdminModel(current_app.db)
        session_service = SessionService(current_app.db)
        
        # Validar refresh token en sesiones
        session = session_service.validate_refresh_token(refresh_token)
        if not session:
            return jsonify({
                "success": False,
                "message": "Refresh token inválido o expirado",
                "data": None
            }), 401
        
        # Obtener datos del admin
        admin = admin_model.get_admin_by_id(current_admin_id)
        if not admin or not admin.get('is_active', True):
            return jsonify({
                "success": False,
                "message": "Administrador no encontrado o desactivado",
                "data": None
            }), 401
        
        # Generar nuevo access token
        tokens = generate_tokens(admin)
        
        return jsonify({
            "success": True,
            "message": "Token renovado exitosamente",
            "data": {
                "access_token": tokens['access_token']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error renovando token: {str(e)}",
            "data": None
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión"""
    try:
        current_admin_id = get_jwt_identity()
        refresh_token = request.json.get('refresh_token') if request.json else None
        
        session_service = SessionService(current_app.db)
        
        if refresh_token:
            # Revocar sesión específica
            session = session_service.validate_refresh_token(refresh_token)
            if session:
                session_service.revoke_session(session['_id'])
        
        return jsonify({
            "success": True,
            "message": "Logout exitoso",
            "data": None
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en logout: {str(e)}",
            "data": None
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_admin():
    """Obtener información del admin actual"""
    try:
        current_admin_id = get_jwt_identity()
        admin_model = AdminModel(current_app.db)
        
        admin = admin_model.get_admin_by_id(current_admin_id)
        if not admin:
            return jsonify({
                "success": False,
                "message": "Administrador no encontrado",
                "data": None
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Información del administrador obtenida",
            "data": admin
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo información: {str(e)}",
            "data": None
        }), 500
