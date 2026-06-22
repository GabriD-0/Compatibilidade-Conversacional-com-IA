from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.extensions import limiter
from app.models import Login
from app.services.auth import authenticate, register_user, delete_user, get_user, list_participants, update_user

bp = Blueprint("auth", __name__)

def _auth_rate_limit() -> str:
    return current_app.config.get("RATE_LIMIT_AUTH")

def _user_payload(user: Login) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "consent_accepted_at": user.consent_accepted_at.isoformat()
        if user.consent_accepted_at
        else None,
    }


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


@bp.get("/me")
@jwt_required()
def me():
    user = get_user(int(get_jwt_identity()))
    return jsonify({"user": _user_payload(user)})


@bp.patch("/me")
@jwt_required()
@limiter.limit(_auth_rate_limit)
def update_me():
    data = request.get_json(silent=True) or {}
    user = update_user(int(get_jwt_identity()), data)
    return jsonify({"user": _user_payload(user)})


@bp.delete("/me")
@jwt_required()
@limiter.limit(_auth_rate_limit)
def delete_me():
    data = request.get_json(silent=True) or {}
    delete_user(int(get_jwt_identity()), data.get("password"))
    return jsonify({"message": "Conta excluida com sucesso."})


@bp.get("/participants")
@jwt_required()
@limiter.limit("60 per minute")
def participants():
    users = list_participants(
        int(get_jwt_identity()),
        search=request.args.get("q", "", type=str),
        limit=request.args.get("limit", 30, type=int),
    )
    return jsonify({"participants": [{"id": user.id, "name": user.name} for user in users]})
