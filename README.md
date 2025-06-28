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
git clone https://github.com/SumajCode/MicroService-Admin.git
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

### Variables de entorno (.env)(Crear)

\`\`\`env
# Aplicación
FLASK_ENV=development
JWT_SECRET_KEY=331b597681934969b6f18b1a60487a64
PORT=4001

# Base de datos
MONGO_URI=mongodb+srv://kevinurena82:kW8x5NlzPioQsqJf@cluster0.ftrgo1z.mongodb.net/microservice_admin?retryWrites=true&w=majority&appName=Cluster0

# CORS
FRONTEND_URL=http://localhost:3003/
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

**Desarrollado con ❤️ por [Kevin Raul Ureña Vidal]**