import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def _bool_env(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def build_sqlalchemy_uri(user: str, password: str, host: str, port: int, database: str) -> str:
    pwd = quote_plus(password or "")
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{database}"


class Config:
    # Mínimo recomendado para HMAC JWT (32+ bytes); sobrescreva em produção.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-secret-replace-in-production-min-32-chars!!")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "30")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_DAYS", "14")))
    JWT_TOKEN_LOCATION = ["headers", "json"]
    JWT_REFRESH_JSON_KEY = "refresh_token"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", "280")),
    }

    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_HOST = os.environ.get("DB_HOST", "")
    DB_PORT = int(os.environ.get("DB_PORT", ""))

    DB_USE_SSH_TUNNEL = _bool_env("DB_USE_SSH_TUNNEL", False)
    SSH_HOST = os.environ.get("SSH_HOST", "")
    SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
    SSH_USERNAME = os.environ.get("SSH_USERNAME", "")
    SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH", "")
    SSH_PASSWORD = os.environ.get("SSH_PASSWORD", "")
    SSH_REMOTE_BIND_ADDRESS = os.environ.get("SSH_REMOTE_BIND_ADDRESS", "")
    SSH_REMOTE_BIND_PORT = int(os.environ.get("SSH_REMOTE_BIND_PORT", ""))
    SSH_LOCAL_BIND_PORT = int(os.environ.get("SSH_LOCAL_BIND_PORT", ""))

    CORS_ORIGINS = [
        o.strip()
        for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if o.strip()
    ]

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = _bool_env("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@localhost")

    PASSWORD_RESET_FRONTEND_URL = os.environ.get(
        "PASSWORD_RESET_FRONTEND_URL", "http://localhost:5173/reset-password"
    )
    PASSWORD_RESET_TOKEN_HOURS = int(os.environ.get("PASSWORD_RESET_TOKEN_HOURS", "1"))

    RATE_LIMIT_AUTH = os.environ.get("RATE_LIMIT_AUTH", "20 per minute")

    DEBUG = False
    LOG_RESET_TOKEN_IN_DEV = _bool_env("LOG_RESET_TOKEN_IN_DEV", True)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    LOG_RESET_TOKEN_IN_DEV = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}