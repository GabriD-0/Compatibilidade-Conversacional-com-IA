from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import limiter
from app.services.analysis import analyze_conversation, get_latest_analysis_for_conversation, get_latest_conversation_analysis
from app.services.conversation import create_conversation, delete_conversation, get_conversation, get_messages, list_conversations

bp = Blueprint("conversations", __name__)

_RATE_READ = "60 per minute"
_RATE_WRITE = "10 per minute"

def _conversation_payload(conv) -> dict:
    latest_analysis = get_latest_analysis_for_conversation(conv.id)
    return {
        "id": conv.id,
        "participant_a": {
            "id": conv.participant_a_id,
            "name": conv.participant_a.name,
        },
        "participant_b": {
            "id": conv.participant_b_id,
            "name": conv.participant_b.name,
        }

        if conv.participant_b
        else None,

        "message_count": conv.message_count,
        "last_message_at": conv.last_message_at.isoformat()

        if conv.last_message_at
        else None,

        "created_at": conv.created_at.isoformat(),
        "score": round(latest_analysis.score) if latest_analysis else None,
        "classification": latest_analysis.classification if latest_analysis else None,
        "last_analysis_at": latest_analysis.computed_at.isoformat() if latest_analysis else None,
    }


def _message_payload(msg) -> dict:
    return {
        "id": msg.id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "sent_at": msg.sent_at.isoformat(),
        "position": msg.position,
        "status": msg.status,
    }


@bp.post("")
@jwt_required()
@limiter.limit(_RATE_WRITE)
def create():
    login_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    conv = create_conversation(login_id, data)
    return jsonify(_conversation_payload(conv)), 201


@bp.get("")
@jwt_required()
@limiter.limit(_RATE_READ)
def list_all():
    login_id = int(get_jwt_identity())
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    items, total = list_conversations(login_id, page=page, per_page=per_page)
    return jsonify(
        {
            "conversations": [_conversation_payload(c) for c in items],
            "total": total,
            "page": page,
            "per_page": per_page,
        }
    )


@bp.get("/<int:conversation_id>")
@jwt_required()
@limiter.limit(_RATE_READ)
def get_one(conversation_id: int):
    login_id = int(get_jwt_identity())
    conv = get_conversation(login_id, conversation_id)
    return jsonify(_conversation_payload(conv))


@bp.get("/<int:conversation_id>/messages")
@jwt_required()
@limiter.limit(_RATE_READ)
def get_msgs(conversation_id: int):
    login_id = int(get_jwt_identity())
    after = request.args.get("after_position", 0, type=int)
    limit = request.args.get("limit", 50, type=int)
    msgs = get_messages(login_id, conversation_id, after_position=after, limit=limit)
    return jsonify({"messages": [_message_payload(m) for m in msgs]})


@bp.delete("/<int:conversation_id>")
@jwt_required()
@limiter.limit(_RATE_WRITE)
def delete(conversation_id: int):
    login_id = int(get_jwt_identity())
    delete_conversation(login_id, conversation_id)
    return jsonify({"message": "Conversa removida com sucesso."})


@bp.post("/<int:conversation_id>/analysis")
@jwt_required()
@limiter.limit(_RATE_WRITE)
def analyze(conversation_id: int):
    login_id = int(get_jwt_identity())
    return jsonify(analyze_conversation(login_id, conversation_id)), 201


@bp.get("/<int:conversation_id>/analysis")
@jwt_required()
@limiter.limit(_RATE_READ)
def get_analysis(conversation_id: int):
    login_id = int(get_jwt_identity())
    return jsonify(get_latest_conversation_analysis(login_id, conversation_id))
