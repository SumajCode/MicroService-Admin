from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import re

class AdminModel:
    def __init__(self, db):
        self.collection = db.admins
        self.create_indexes()
    
    def create_indexes(self):
        """Crear índices para optimizar consultas"""
        try:
            self.collection.create_index("email", unique=True)
            self.collection.create_index("username", unique=True)
        except Exception as e:
            print(f"Índices ya existen o error: {e}")
    
    def validate_email(self, email):
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validar fortaleza de contraseña"""
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        if not re.search(r'[A-Za-z]', password):
            return False, "La contraseña debe contener al menos una letra"
        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"
        return True, "Contraseña válida"
    
    def create_admin(self, data):
        """Crear nuevo administrador"""
        try:
            # Validaciones
            if not self.validate_email(data.get('email', '')):
                return None, "Email inválido"
            
            is_valid, message = self.validate_password(data.get('password', ''))
            if not is_valid:
                return None, message
            
            # Verificar si ya existe
            if self.collection.find_one({"email": data['email']}):
                return None, "El email ya está registrado"
            
            if self.collection.find_one({"username": data['username']}):
                return None, "El username ya está registrado"
            
            # Crear admin
            admin_data = {
                "username": data['username'],
                "email": data['email'],
                "password": generate_password_hash(data['password']),
                "first_name": data.get('first_name', ''),
                "last_name": data.get('last_name', ''),
                "role": data.get('role', 'admin'),
                "is_active": data.get('is_active', True),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = self.collection.insert_one(admin_data)
            admin_data['_id'] = str(result.inserted_id)
            admin_data.pop('password')  # No devolver la contraseña
            
            return admin_data, "Administrador creado exitosamente"
            
        except Exception as e:
            return None, f"Error creando administrador: {str(e)}"
    
    def get_admin_by_id(self, admin_id):
        """Obtener administrador por ID"""
        try:
            admin = self.collection.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin['_id'] = str(admin['_id'])
                admin.pop('password', None)
                return admin
            return None
        except Exception as e:
            print(f"Error obteniendo admin: {e}")
            return None
    
    def get_admin_by_email(self, email):
        """Obtener administrador por email (incluye password para auth)"""
        try:
            admin = self.collection.find_one({"email": email})
            if admin:
                admin['_id'] = str(admin['_id'])
                return admin
            return None
        except Exception as e:
            print(f"Error obteniendo admin por email: {e}")
            return None
    
    def get_all_admins(self, page=1, limit=10):
        """Obtener todos los administradores con paginación"""
        try:
            skip = (page - 1) * limit
            admins = list(self.collection.find({}, {"password": 0})
                         .skip(skip).limit(limit).sort("created_at", -1))
            
            for admin in admins:
                admin['_id'] = str(admin['_id'])
            
            total = self.collection.count_documents({})
            
            return {
                "admins": admins,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        except Exception as e:
            print(f"Error obteniendo admins: {e}")
            return None
    
    def update_admin(self, admin_id, data):
        """Actualizar administrador"""
        try:
            update_data = {
                "updated_at": datetime.utcnow()
            }
            
            # Campos permitidos para actualizar
            allowed_fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
            for field in allowed_fields:
                if field in data:
                    if field == 'email' and not self.validate_email(data[field]):
                        return None, "Email inválido"
                    update_data[field] = data[field]
            
            # Actualizar contraseña si se proporciona
            if 'password' in data:
                is_valid, message = self.validate_password(data['password'])
                if not is_valid:
                    return None, message
                update_data['password'] = generate_password_hash(data['password'])
            
            result = self.collection.update_one(
                {"_id": ObjectId(admin_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated_admin = self.get_admin_by_id(admin_id)
                return updated_admin, "Administrador actualizado exitosamente"
            else:
                return None, "Administrador no encontrado"
                
        except Exception as e:
            return None, f"Error actualizando administrador: {str(e)}"
    
    def delete_admin(self, admin_id):
        """Eliminar administrador"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(admin_id)})
            if result.deleted_count > 0:
                return True, "Administrador eliminado exitosamente"
            else:
                return False, "Administrador no encontrado"
        except Exception as e:
            return False, f"Error eliminando administrador: {str(e)}"
    
    def verify_password(self, email, password):
        """Verificar contraseña para login"""
        try:
            admin = self.get_admin_by_email(email)
            if admin and check_password_hash(admin['password'], password):
                admin.pop('password')  # Remover password del resultado
                return admin
            return None
        except Exception as e:
            print(f"Error verificando contraseña: {e}")
            return None
