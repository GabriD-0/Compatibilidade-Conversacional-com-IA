import os
from dotenv import load_dotenv

# TODO: Reavaliar config

load_dotenv()

class Config:
    """Configuração base."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://localhost/compatibilidade_db"
    )
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento."""
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Configuração de produção."""
    DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
