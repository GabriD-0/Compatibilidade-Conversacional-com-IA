import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# Função auxiliar para converter variáveis de ambiente booleanas
def _bool_env(name: str, default: bool = False) -> bool:
    env_value = os.environ.get(name)
    if env_value is None:
        return default
    return env_value.strip().lower() in ("1", "true", "yes", "on")

def build_sqlalchemy_uri(user: str, password: str, host: str, port: int, database: str) -> str:
    encoded_password = quote_plus(password or "")
    return f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}"

class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "chave-secreta-do-jwt")
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "120")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_DAYS", "15")))
    JWT_TOKEN_LOCATION = ["headers", "json"]
    JWT_REFRESH_JSON_KEY = "refresh_token"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", "280")),
    }

    DB_USER = os.environ.get("DB_USER", "")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_HOST = os.environ.get("DB_HOST", "")
    DB_PORT = int(os.environ.get("DB_PORT", ""))

    DB_USE_SSH_TUNNEL = _bool_env("DB_USE_SSH_TUNNEL", False)
    SSH_HOST = os.environ.get("SSH_HOST", "")
    SSH_PORT = int(os.environ.get("SSH_PORT", ""))
    SSH_USERNAME = os.environ.get("SSH_USERNAME", "")
    SSH_PASSWORD = os.environ.get("SSH_PASSWORD", "")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS").split(",")
        if origin.strip()
    ]

    RATE_LIMIT_AUTH = "20 per minute"
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}