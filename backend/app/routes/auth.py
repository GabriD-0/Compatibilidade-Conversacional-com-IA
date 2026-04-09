from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.extensions import limiter
from app.models import Login
from app.services.auth_service import authenticate, register_user

bp = Blueprint("auth", __name__)

def _auth_rate_limit() -> str:
    return current_app.config.get("RATE_LIMIT_AUTH")

def _user_payload(user: Login) -> dict:
    return {"id": user.id, "email": user.email, "name": user.name}


@bp.post("/register")
@limiter.limit(_auth_rate_limit)
def register():
    data = request.get_json(silent=True) or {}
    user = register_user(data)
    identity = str(user.id)
    access = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    return (
        jsonify(
            {
                "user": _user_payload(user),
                "access_token": access,
                "refresh_token": refresh,
            }
        ),
        201,
    )


@bp.post("/login")
@limiter.limit(_auth_rate_limit)
def login():
    data = request.get_json(silent=True) or {}
    user = authenticate(data)
    identity = str(user.id)
    access = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    return jsonify(
        {
            "user": _user_payload(user),
            "access_token": access,
            "refresh_token": refresh,
        }
    )


@bp.post("/refresh")
@jwt_required(refresh=True)
@limiter.limit(_auth_rate_limit)
def refresh():
    uid = get_jwt_identity()
    access = create_access_token(identity=str(uid))
    return jsonify({"access_token": access})