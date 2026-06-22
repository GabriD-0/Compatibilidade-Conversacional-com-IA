from flask import jsonify
from flask_jwt_extended import JWTManager
from app.errors import ApiError
from app.extensions import db
from app.models import Login

def register_jwt_handlers(jwt: JWTManager) -> None:
    @jwt.unauthorized_loader
    def unauthorized_callback(msg: str):
        return (
            jsonify(
                {
                    "error": {
                        "code": "unauthorized",
                        "message": msg or "Autenticação necessária.",
                    }
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(msg: str):
        return (
            jsonify(
                {
                    "error": {
                        "code": "invalid_token",
                        "message": msg or "Token inválido.",
                    }
                }
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {
                    "error": {
                        "code": "token_expired",
                        "message": "Token expirado. Faça login novamente.",
                    }
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def needs_fresh_callback(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {
                    "error": {
                        "code": "fresh_token_required",
                        "message": "Token fresco necessário para esta operação.",
                    }
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {
                    "error": {
                        "code": "token_revoked",
                        "message": "Token revogado.",
                    }
                }
            ),
            401,
        )

def register_jwt_user_lookup(jwt: JWTManager) -> None:
    @jwt.user_lookup_loader
    def load_current_user(_jwt_header, jwt_data):
        try:
            return db.session.get(Login, int(jwt_data["sub"]))
        except (KeyError, TypeError, ValueError):
            return None

    @jwt.user_lookup_error_loader
    def user_lookup_error(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {
                    "error": {
                        "code": "user_not_found",
                        "message": "A conta associada a este token nao existe mais.",
                    }
                }
            ),
            401,
        )

def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        body = {"error": {"code": err.code, "message": err.message}}
        if err.details:
            body["error"]["details"] = err.details
        return jsonify(body), err.status_code

    @app.errorhandler(429)
    def handle_rate_limit(e):
        return (
            jsonify(
                {
                    "error": {
                        "code": "rate_limit",
                        "message": "Muitas requisições. Tente novamente em instantes.",
                    }
                }
            ),
            429,
        )