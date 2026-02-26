from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import config_by_name

# TODO: Reavaliar services

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    env = config_name or __config_from_env()
    app.config.from_object(config_by_name[env])

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    # Importar modelos para Flask-Migrate
    from app import models  # noqa: F401

    from app.routes.dialogos import bp as dialogos_bp
    from app.routes.dados import bp as dados_bp

    app.register_blueprint(dialogos_bp, url_prefix="/api/v1")
    app.register_blueprint(dados_bp, url_prefix="/api/v1")

    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app


def __config_from_env():
    import os
    return os.environ.get("FLASK_ENV", "development")
