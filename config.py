import os
from datetime import timedelta
from dotenv import load_dotenv
from flask_appbuilder.security.manager import AUTH_DB

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave-en-el-env")
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost:3309/inventario_ventas?charset=utf8mb4",
)
CSRF_ENABLED = True

APP_NAME = "Inventario y Ventas"
AUTH_TYPE = AUTH_DB

BABEL_DEFAULT_LOCALE = "es"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "es": {"flag": "es", "name": "Español"},
    "en": {"flag": "gb", "name": "English"},
}


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


# --- Seguridad ---
AUTH_USER_REGISTRATION = False
AUTH_ROLE_ADMIN = "Admin"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"