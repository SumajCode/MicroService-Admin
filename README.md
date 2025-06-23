# 🚀 MicroService Admin - Backend

Backend modular en Python con Flask y MongoDB para gestionar usuarios administradores. Diseñado para ser consumido por un frontend en React con autenticación JWT, gestión de sesiones y despliegue en Render.com.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Pruebas](#-pruebas)
- [Despliegue](#-despliegue)
- [Contribución](#-contribución)

## ✨ Características

- 🔐 **Autenticación JWT** con Access y Refresh tokens
- 👥 **CRUD completo** para administradores
- 🔄 **Gestión de sesiones** con seguimiento de dispositivos
- 🛡️ **Seguridad robusta** con validaciones y encriptación
- 🧪 **Pruebas automatizadas** con pytest
- 🔄 **CI/CD** con GitHub Actions
- 🌐 **CORS configurado** para React
- 📊 **MongoDB** como base de datos
- 🚀 **Despliegue en Render.com**

## 📁 Estructura del Proyecto

\`\`\`
MicroService-Admin/
├── src/
│   ├── app.py                 # Aplicación principal
│   ├── routes/
│   │   ├── admin.py          # Rutas CRUD administradores
│   │   ├── auth.py           # Rutas de autenticación
│   │   └── session.py        # Rutas de sesiones
│   ├── models/
│   │   ├── admin.py          # Modelo de administrador
│   │   └── session.py        # Modelo de sesión
│   ├── services/
│   │   └── session.py        # Servicio de sesiones
│   ├── auth/
│   │   └── jwt_utils.py      # Utilidades JWT
│   └── __init__.py
├── tests/
│   └── test_helper.py        # Pruebas unitarias
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions
├── .env                      # Variables de entorno
├── requirements.txt          # Dependencias Python
├── render.yaml              # Configuración Render
└── README.md
\`\`\`

## 🛠️ Instalación

### Prerrequisitos

- Python 3.11+
- MongoDB 7.0+
- Git

### Pasos de instalación

1. **Clonar el repositorio**
\`\`\`bash
git clone https://github.com/tu-usuario/MicroService-Admin.git
cd MicroService-Admin
\`\`\`

2. **Crear entorno virtual**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
\`\`\`

3. **Instalar dependencias**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Configurar variables de entorno**
\`\`\`bash
cp .env.example .env
# Editar .env con tus configuraciones
\`\`\`

## ⚙️ Configuración

### Variables de entorno (.env)

\`\`\`env
# Aplicación
FLASK_ENV=development
JWT_SECRET_KEY=your-super-secret-jwt-key
PORT=5000

# Base de datos
MONGO_URI=mongodb://localhost:27017/admin_db

# CORS
FRONTEND_URL=http://localhost:3000
\`\`\`

### MongoDB

Asegúrate de tener MongoDB ejecutándose:

\`\`\`bash
# Instalar MongoDB (Ubuntu/Debian)
sudo apt-get install mongodb

# Iniciar servicio
sudo systemctl start mongodb
sudo systemctl enable mongodb
\`\`\`

## 🚀 Uso

### Desarrollo

\`\`\`bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar aplicación
python src/app.py
\`\`\`

La aplicación estará disponible en \`http://localhost:5000\`

### Producción

\`\`\`bash
gunicorn --bind 0.0.0.0:5000 src.app:create_app()
\`\`\`

## 📚 API Endpoints

### 🔐 Autenticación

#### POST /api/auth/login
Iniciar sesión de administrador.

**✅ Ejemplo exitoso:**
\`\`\`http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "123456"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "admin": {
      "_id": "507f1f77bcf86cd799439011",
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "Admin",
      "last_name": "User",
      "role": "admin",
      "is_active": true
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "wrong_password"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Credenciales inválidas",
  "data": null
}
\`\`\`

#### POST /api/auth/refresh
Renovar access token.

**✅ Ejemplo exitoso:**
\`\`\`http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Token renovado exitosamente",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
POST /api/auth/refresh
Authorization: Bearer <invalid_or_expired_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Refresh token inválido o expirado",
  "data": null
}
\`\`\`

#### GET /api/auth/me
Obtener información del administrador actual.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/auth/me
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Información del administrador obtenida",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
GET /api/auth/me
Authorization: Bearer <invalid_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Token inválido",
  "data": null
}
\`\`\`

### 👥 Administradores

#### POST /api/admins/
Crear nuevo administrador.

**✅ Ejemplo exitoso:**
\`\`\`http
POST /api/admins/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "newadmin",
  "email": "newadmin@example.com",
  "password": "securepass123",
  "first_name": "New",
  "last_name": "Admin",
  "role": "admin"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Administrador creado exitosamente",
  "data": {
    "_id": "507f1f77bcf86cd799439012",
    "username": "newadmin",
    "email": "newadmin@example.com",
    "first_name": "New",
    "last_name": "Admin",
    "role": "admin",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
POST /api/admins/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@example.com",
  "password": "123"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "El email ya está registrado",
  "data": null
}
\`\`\`

#### GET /api/admins/
Obtener lista de administradores.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/admins/?page=1&limit=10
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Administradores obtenidos exitosamente",
  "data": {
    "admins": [
      {
        "_id": "507f1f77bcf86cd799439011",
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "total_pages": 1
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
GET /api/admins/
Authorization: Bearer <invalid_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Token inválido",
  "data": null
}
\`\`\`

#### GET /api/admins/{id}
Obtener administrador por ID.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/admins/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Administrador encontrado",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
GET /api/admins/invalid_id
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Administrador no encontrado",
  "data": null
}
\`\`\`

#### PUT /api/admins/{id}
Actualizar administrador.

**✅ Ejemplo exitoso:**
\`\`\`http
PUT /api/admins/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Admin",
  "role": "super_admin"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Administrador actualizado exitosamente",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Updated",
    "last_name": "Admin",
    "role": "super_admin",
    "is_active": true,
    "updated_at": "2024-01-15T11:30:00Z"
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
PUT /api/admins/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "invalid-email"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Email inválido",
  "data": null
}
\`\`\`

#### DELETE /api/admins/{id}
Eliminar administrador.

**✅ Ejemplo exitoso:**
\`\`\`http
DELETE /api/admins/507f1f77bcf86cd799439012
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Administrador eliminado exitosamente",
  "data": null
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
DELETE /api/admins/507f1f77bcf86cd799439011
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "No puedes eliminar tu propia cuenta",
  "data": null
}
\`\`\`

### 🔄 Sesiones

#### GET /api/sessions/
Obtener sesiones del administrador actual.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/sessions/?page=1&limit=5
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Sesiones obtenidas exitosamente",
  "data": {
    "sessions": [
      {
        "_id": "507f1f77bcf86cd799439013",
        "admin_id": "507f1f77bcf86cd799439011",
        "user_agent": "Mozilla/5.0...",
        "ip_address": "192.168.1.100",
        "created_at": "2024-01-15T10:30:00Z",
        "last_used": "2024-01-15T11:30:00Z",
        "is_active": true
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 5,
    "total_pages": 1
  }
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
GET /api/sessions/
Authorization: Bearer <expired_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Token expirado",
  "data": null
}
\`\`\`

#### DELETE /api/sessions/{id}
Revocar sesión específica.

**✅ Ejemplo exitoso:**
\`\`\`http
DELETE /api/sessions/507f1f77bcf86cd799439013
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Sesión revocada exitosamente",
  "data": null
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
DELETE /api/sessions/invalid_session_id
Authorization: Bearer <access_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Sesión no encontrada",
  "data": null
}
\`\`\`

#### POST /api/sessions/revoke-all
Revocar todas las sesiones excepto la actual.

**✅ Ejemplo exitoso:**
\`\`\`http
POST /api/sessions/revoke-all
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "except_token": "current_refresh_token"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "3 sesiones revocadas",
  "data": null
}
\`\`\`

**❌ Ejemplo fallido:**
\`\`\`http
POST /api/sessions/revoke-all
Authorization: Bearer <invalid_token>
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": false,
  "message": "Token inválido",
  "data": null
}
\`\`\`

### 🔧 Utilidades

#### GET /api/health
Verificar estado del servidor.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/health
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Servidor funcionando correctamente",
  "data": {
    "status": "healthy"
  }
}
\`\`\`

#### GET /api/helper
Endpoint de ayuda para pruebas.

**✅ Ejemplo exitoso:**
\`\`\`http
GET /api/helper
\`\`\`

**Respuesta:**
\`\`\`json
{
  "success": true,
  "message": "Helper endpoint funcionando",
  "data": {
    "version": "1.0.0",
    "service": "admin-microservice"
  }
}
\`\`\`

## 🧪 Pruebas

### Ejecutar pruebas

\`\`\`bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas
python -m pytest tests/ -v

# Ejecutar con cobertura
pip install coverage
coverage run -m pytest tests/
coverage report -m
coverage html
\`\`\`

### Estructura de pruebas

\`\`\`
tests/
├── test_helper.py          # Pruebas del endpoint helper
├── test_auth.py           # Pruebas de autenticación (opcional)
├── test_admin.py          # Pruebas CRUD administradores (opcional)
└── test_session.py        # Pruebas de sesiones (opcional)
\`\`\`

### Ejemplo de prueba

\`\`\`python
def test_helper_endpoint_success(client):
    """Test exitoso del endpoint /helper"""
    response = client.get('/api/helper')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == "Helper endpoint funcionando"
    assert data['data']['version'] == "1.0.0"
\`\`\`

## 🚀 Despliegue

### Render.com

1. **Conectar repositorio**
   - Conecta tu repositorio de GitHub a Render
   - Selecciona el archivo \`render.yaml\`

2. **Configurar variables de entorno**
   \`\`\`env
   FLASK_ENV=production
   JWT_SECRET_KEY=your-production-secret-key
   MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/admin_db
   FRONTEND_URL=https://your-frontend-domain.com
   \`\`\`

3. **Desplegar**
   - Render detectará automáticamente la configuración
   - El despliegue se ejecutará automáticamente

### Docker (Opcional)

\`\`\`dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .env .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:create_app()"]
\`\`\`

## 🔒 Seguridad

### Características de seguridad implementadas

- ✅ **Autenticación JWT** con tokens de acceso y renovación
- ✅ **Encriptación de contraseñas** con Werkzeug
- ✅ **Validación de entrada** en todos los endpoints
- ✅ **CORS configurado** para dominios específicos
- ✅ **Gestión de sesiones** con seguimiento de dispositivos
- ✅ **Tokens seguros** con expiración automática
- ✅ **Validación de email** con expresiones regulares
- ✅ **Prevención de auto-eliminación** de administradores

### Recomendaciones adicionales

- Usar HTTPS en producción
- Configurar rate limiting
- Implementar logging de seguridad
- Usar variables de entorno para secretos
- Actualizar dependencias regularmente

## 🤝 Contribución

### Proceso de contribución

1. **Fork del repositorio**
2. **Crear rama de feature**
   \`\`\`bash
   git checkout -b feature/nueva-funcionalidad
   \`\`\`
3. **Realizar cambios y commits**
   \`\`\`bash
   git commit -m "feat: agregar nueva funcionalidad"
   \`\`\`
4. **Ejecutar pruebas**
   \`\`\`bash
   python -m pytest tests/ -v
   \`\`\`
5. **Push y crear Pull Request**

### Estándares de código

- Seguir PEP 8 para Python
- Documentar funciones y clases
- Escribir pruebas para nuevas funcionalidades
- Usar commits semánticos

### Reportar bugs

Usa el sistema de issues de GitHub con:
- Descripción detallada del problema
- Pasos para reproducir
- Entorno (OS, Python version, etc.)
- Logs de error

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo \`LICENSE\` para más detalles.

## 📞 Soporte

- **Email**: support@microservice-admin.com
- **GitHub Issues**: [Crear issue](https://github.com/tu-usuario/MicroService-Admin/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/MicroService-Admin/wiki)

---

**Desarrollado con ❤️ por [Tu Nombre]**

*¿Te gusta este proyecto? ¡Dale una ⭐ en GitHub!*
