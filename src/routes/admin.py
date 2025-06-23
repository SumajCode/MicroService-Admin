from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.admin import AdminModel

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['POST'])
@jwt_required()
def create_admin():
    """Crear nuevo administrador"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Username, email y password son requeridos",
                "data": None
            }), 400
        
        admin_model = AdminModel(current_app.db)
        admin_data, message = admin_model.create_admin(data)
        
        if admin_data:
            return jsonify({
                "success": True,
                "message": message,
                "data": admin_data
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": message,
                "data": None
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error creando administrador: {str(e)}",
            "data": None
        }), 500

@admin_bp.route('/', methods=['GET'])
@jwt_required()
def get_admins():
    """Obtener lista de administradores"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        admin_model = AdminModel(current_app.db)
        result = admin_model.get_all_admins(page, limit)
        
        if result:
            return jsonify({
                "success": True,
                "message": "Administradores obtenidos exitosamente",
                "data": result
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Error obteniendo administradores",
                "data": None
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo administradores: {str(e)}",
            "data": None
        }), 500

@admin_bp.route('/<admin_id>', methods=['GET'])
@jwt_required()
def get_admin(admin_id):
    """Obtener administrador por ID"""
    try:
        admin_model = AdminModel(current_app.db)
        admin = admin_model.get_admin_by_id(admin_id)
        
        if admin:
            return jsonify({
                "success": True,
                "message": "Administrador encontrado",
                "data": admin
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Administrador no encontrado",
                "data": None
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo administrador: {str(e)}",
            "data": None
        }), 500

@admin_bp.route('/<admin_id>', methods=['PUT'])
@jwt_required()
def update_admin(admin_id):
    """Actualizar administrador"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No se proporcionaron datos para actualizar",
                "data": None
            }), 400
        
        admin_model = AdminModel(current_app.db)
        admin_data, message = admin_model.update_admin(admin_id, data)
        
        if admin_data:
            return jsonify({
                "success": True,
                "message": message,
                "data": admin_data
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": message,
                "data": None
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error actualizando administrador: {str(e)}",
            "data": None
        }), 500

@admin_bp.route('/<admin_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(admin_id):
    """Eliminar administrador"""
    try:
        current_admin_id = get_jwt_identity()
        
        # Evitar que un admin se elimine a sí mismo
        if current_admin_id == admin_id:
            return jsonify({
                "success": False,
                "message": "No puedes eliminar tu propia cuenta",
                "data": None
            }), 400
        
        admin_model = AdminModel(current_app.db)
        success, message = admin_model.delete_admin(admin_id)
        
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
            "message": f"Error eliminando administrador: {str(e)}",
            "data": None
        }), 500
