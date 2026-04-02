import logging
import importlib
from flask import Flask
from app.config import build_sqlalchemy_uri, config_by_name
from app.db_tunnel import start_ssh_tunnel
from app.errors.handlers import register_error_handlers, register_jwt_handlers
from app.extensions import cors, db, jwt, limiter, mail, migrate
from app.routes.auth import bp as auth_bp
from app.routes.health import bp as health_bp

log = logging.getLogger(__name__)


def create_app(config_name: str | None = None) -> Flask:
    flask_app = Flask(__name__)

    name = (config_name or "development").lower()
    cfg = config_by_name.get(name, config_by_name["development"])
    flask_app.config.from_object(cfg)

    local_port = start_ssh_tunnel(flask_app.config)
    if local_port is not None:
        host, port = "127.0.0.1", local_port
    else:
        host = flask_app.config["DB_HOST"]
        port = flask_app.config["DB_PORT"]

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = build_sqlalchemy_uri(
        flask_app.config["DB_USER"],
        flask_app.config["DB_PASSWORD"],
        host,
        port,
        flask_app.config["DB_NAME"],
    )

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)
    register_jwt_handlers(jwt)
    mail.init_app(flask_app)
    limiter.init_app(flask_app)
    origins = flask_app.config["CORS_ORIGINS"]

    cors.init_app(
        flask_app,
        resources={
            r"/api/*": {"origins": origins},
            r"/health": {"origins": origins},
        },
        supports_credentials=True,
    )

    register_error_handlers(flask_app)

    flask_app.register_blueprint(health_bp)
    flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")

    importlib.import_module("app.models")

    return flask_app