from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import limiter
from app.services.dashboard import get_dashboard_summary

bp = Blueprint("dashboard", __name__)

RATE_READ = "60 per minute"

@bp.get("")
@jwt_required()
@limiter.limit(RATE_READ)
def get_summary():
    login_id = int(get_jwt_identity())
    return jsonify(get_dashboard_summary(login_id))
