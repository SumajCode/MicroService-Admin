from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.session import SessionService

session_bp = Blueprint('session', __name__)

@session_bp.route('/', methods=['GET'])
@jwt_required()
def get_sessions():
    """Obtener sesiones del administrador actual"""
    try:
        current_admin_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        session_service = SessionService(current_app.db)
        result = session_service.get_admin_sessions(current_admin_id, page, limit)
        
        if result:
            return jsonify({
                "success": True,
                "message": "Sesiones obtenidas exitosamente",
                "data": result
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Error obteniendo sesiones",
                "data": None
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo sesiones: {str(e)}",
            "data": None
        }), 500

@session_bp.route('/<session_id>', methods=['DELETE'])
@jwt_required()
def revoke_session(session_id):
    """Revocar sesión específica"""
    try:
        session_service = SessionService(current_app.db)
        success, message = session_service.revoke_session(session_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": message,
                "data": None
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": message,
                "data": None
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error revocando sesión: {str(e)}",
            "data": None
        }), 500

@session_bp.route('/revoke-all', methods=['POST'])
@jwt_required()
def revoke_all_sessions():
    """Revocar todas las sesiones excepto la actual"""
    try:
        current_admin_id = get_jwt_identity()
        data = request.get_json() or {}
        except_token = data.get('except_token')
        
        session_service = SessionService(current_app.db)
        success, message = session_service.revoke_all_sessions(current_admin_id, except_token)
        
        return jsonify({
            "success": success,
            "message": message,
            "data": None
        }), 200 if success else 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error revocando sesiones: {str(e)}",
            "data": None
        }), 500

@session_bp.route('/cleanup', methods=['POST'])
@jwt_required()
def cleanup_sessions():
    """Limpiar sesiones expiradas (solo para admins)"""
    try:
        session_service = SessionService(current_app.db)
        cleaned_count = session_service.cleanup_expired()
        
        return jsonify({
            "success": True,
            "message": f"Se limpiaron {cleaned_count} sesiones expiradas",
            "data": {"cleaned_count": cleaned_count}
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error limpiando sesiones: {str(e)}",
            "data": None
        }), 500
