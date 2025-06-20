from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    
    # Configurar CORS para React
    CORS(app, 
         origins=os.getenv('FRONTEND_URL',),
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'])
    
    # Inicializar JWT
    jwt = JWTManager(app)
    
    # Configurar MongoDB
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
        app.db = db
        print("✅ Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        raise e
    
    # Registrar blueprints
    from src.routes.admin import admin_bp
    from src.routes.auth import auth_bp
    from src.routes.session import session_bp
    
    app.register_blueprint(admin_bp, url_prefix='/api/admins')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    
    # Endpoint de salud
    @app.route('/api/health')
    def health_check():
        return {
            "success": True,
            "message": "Servidor funcionando correctamente",
            "data": {"status": "healthy"}
        }
    
    # Endpoint helper para pruebas
    @app.route('/api/helper')
    def helper():
        return {
            "success": True,
            "message": "Helper endpoint funcionando",
            "data": {"version": "1.0.0", "service": "admin-microservice"}
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
