from datetime import datetime, timedelta
from bson import ObjectId

class SessionModel:
    def __init__(self, db):
        self.collection = db.sessions
        self.create_indexes()
    
    def create_indexes(self):
        """Crear índices para optimizar consultas"""
        try:
            self.collection.create_index("admin_id")
            self.collection.create_index("refresh_token", unique=True)
            self.collection.create_index("expires_at", expireAfterSeconds=0)
        except Exception as e:
            print(f"Índices ya existen o error: {e}")
    
    def create_session(self, admin_id, refresh_token, user_agent=None, ip_address=None):
        """Crear nueva sesión"""
        try:
            session_data = {
                "admin_id": admin_id,
                "refresh_token": refresh_token,
                "user_agent": user_agent,
                "ip_address": ip_address,
                "created_at": datetime.utcnow(),
                "last_used": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=30),
                "is_active": True
            }
            
            result = self.collection.insert_one(session_data)
            session_data['_id'] = str(result.inserted_id)
            
            return session_data, "Sesión creada exitosamente"
            
        except Exception as e:
            return None, f"Error creando sesión: {str(e)}"
    
    def get_session_by_token(self, refresh_token):
        """Obtener sesión por refresh token"""
        try:
            session = self.collection.find_one({
                "refresh_token": refresh_token,
                "is_active": True,
                "expires_at": {"$gt": datetime.utcnow()}
            })
            
            if session:
                session['_id'] = str(session['_id'])
                # Actualizar último uso
                self.collection.update_one(
                    {"_id": ObjectId(session['_id'])},
                    {"$set": {"last_used": datetime.utcnow()}}
                )
                return session
            return None
            
        except Exception as e:
            print(f"Error obteniendo sesión: {e}")
            return None
    
    def get_admin_sessions(self, admin_id, page=1, limit=10):
        """Obtener sesiones de un administrador"""
        try:
            skip = (page - 1) * limit
            sessions = list(self.collection.find(
                {"admin_id": admin_id},
                {"refresh_token": 0}  # No devolver el token
            ).skip(skip).limit(limit).sort("last_used", -1))
            
            for session in sessions:
                session['_id'] = str(session['_id'])
            
            total = self.collection.count_documents({"admin_id": admin_id})
            
            return {
                "sessions": sessions,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
            
        except Exception as e:
            print(f"Error obteniendo sesiones: {e}")
            return None
    
    def revoke_session(self, session_id):
        """Revocar sesión específica"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"is_active": False, "revoked_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                return True, "Sesión revocada exitosamente"
            else:
                return False, "Sesión no encontrada"
                
        except Exception as e:
            return False, f"Error revocando sesión: {str(e)}"
    
    def revoke_all_sessions(self, admin_id, except_token=None):
        """Revocar todas las sesiones de un admin excepto la actual"""
        try:
            query = {"admin_id": admin_id, "is_active": True}
            if except_token:
                query["refresh_token"] = {"$ne": except_token}
            
            result = self.collection.update_many(
                query,
                {"$set": {"is_active": False, "revoked_at": datetime.utcnow()}}
            )
            
            return True, f"{result.modified_count} sesiones revocadas"
            
        except Exception as e:
            return False, f"Error revocando sesiones: {str(e)}"
    
    def cleanup_expired_sessions(self):
        """Limpiar sesiones expiradas"""
        try:
            result = self.collection.delete_many({
                "expires_at": {"$lt": datetime.utcnow()}
            })
            return result.deleted_count
        except Exception as e:
            print(f"Error limpiando sesiones: {e}")
            return 0
