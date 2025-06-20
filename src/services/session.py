from src.models.session import SessionModel
from src.auth.jwt_utils import generate_secure_token
from flask import request

class SessionService:
    def __init__(self, db):
        self.session_model = SessionModel(db)
    
    def create_session(self, admin_id, refresh_token):
        """Crear nueva sesión con información del request"""
        user_agent = request.headers.get('User-Agent', 'Unknown')
        ip_address = request.remote_addr or 'Unknown'
        
        return self.session_model.create_session(
            admin_id=admin_id,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address
        )
    
    def validate_refresh_token(self, refresh_token):
        """Validar refresh token y obtener sesión"""
        return self.session_model.get_session_by_token(refresh_token)
    
    def get_admin_sessions(self, admin_id, page=1, limit=10):
        """Obtener sesiones de un administrador"""
        return self.session_model.get_admin_sessions(admin_id, page, limit)
    
    def revoke_session(self, session_id):
        """Revocar sesión específica"""
        return self.session_model.revoke_session(session_id)
    
    def revoke_all_sessions(self, admin_id, except_token=None):
        """Revocar todas las sesiones excepto la actual"""
        return self.session_model.revoke_all_sessions(admin_id, except_token)
    
    def cleanup_expired(self):
        """Limpiar sesiones expiradas"""
        return self.session_model.cleanup_expired_sessions()
