import logging
import time
from flask import request, session
from flask_jwt_extended import decode_token
from flask_socketio import emit, join_room, leave_room
from app.errors import ApiError
from app.services.conversation_service import get_conversation, get_conversation, mark_read, persist_message

log = logging.getLogger(__name__)

_MSG_INTERVAL = 1.0
_last_msg_time: dict[str, float] = {}


def register_handlers(socketio) -> None:
    @socketio.on("connect")
    def on_connect(auth):
        token = None

        if isinstance(auth, dict):
            token = auth.get("token")

        if not token:
            token = request.args.get("token", "")

        if not token:
            log.warning("WebSocket rejeitado: sem token (sid=%s)", request.sid)
            return False

        try:
            data = decode_token(token)
            session["user_id"] = int(data["sub"])
            log.info(
                "WebSocket conectado: user_id=%s sid=%s",
                session["user_id"],
                request.sid,
            )

        except Exception as exc:
            log.warning(
                "WebSocket rejeitado: token inválido sid=%s erro=%s",
                request.sid,
                exc,
            )
            return False

    @socketio.on("disconnect")
    def on_disconnect():
        _last_msg_time.pop(request.sid, None)
        log.info("WebSocket desconectado: sid=%s", request.sid)

    @socketio.on("join")
    def on_join(data):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "unauthorized"}

        conversation_id = data.get("conversation_id")
        if not conversation_id:
            return {"error": "missing_conversation_id"}

        try:
            get_conversation(user_id, conversation_id)

        except ApiError:
            return {"error": "not_found"}

        room = f"conv_{conversation_id}"
        join_room(room)
        emit("user_joined", {"user_id": user_id}, room=room, skip_sid=request.sid)
        log.info("User %s entrou na sala %s", user_id, room)
        return {"ok": True}

    @socketio.on("leave")
    def on_leave(data):
        conversation_id = data.get("conversation_id")
        if conversation_id:
            leave_room(f"conv_{conversation_id}")

    @socketio.on("send_message")
    def on_send_message(data):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "unauthorized"}

        # Rate limit: 1 msg/s por conexão
        now = time.monotonic()
        if now - _last_msg_time.get(request.sid, 0) < _MSG_INTERVAL:
            return {"error": "rate_limited"}
        _last_msg_time[request.sid] = now

        conversation_id = data.get("conversation_id")
        content = data.get("content", "")

        if not conversation_id:
            return {"error": "missing_conversation_id"}

        try:
            get_conversation(user_id, conversation_id)

        except ApiError:
            return {"error": "not_found"}

        try:
            msg = persist_message(conversation_id, user_id, content)

        except ApiError as exc:
            return {"error": exc.code, "message": exc.message}

        payload = {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "sent_at": msg.sent_at.isoformat(),
            "position": msg.position,
            "status": msg.status,
        }
        room = f"conv_{conversation_id}"
        emit("new_message", payload, room=room)
        return {"ok": True, "position": msg.position}

    @socketio.on("typing")
    def on_typing(data):
        user_id = session.get("user_id")
        if not user_id:
            return

        conversation_id = data.get("conversation_id")
        if conversation_id:
            emit(
                "user_typing",
                {"sender_id": user_id},
                room=f"conv_{conversation_id}",
                skip_sid=request.sid,
            )

    @socketio.on("read")
    def on_read(data):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "unauthorized"}

        conversation_id = data.get("conversation_id")
        up_to_position = data.get("up_to_position")

        if conversation_id is None or up_to_position is None:
            return {"error": "missing_fields"}

        try:
            get_conversation(user_id, conversation_id)

        except ApiError:
            return {"error": "not_found"}

        mark_read(conversation_id, user_id, up_to_position)

        emit(
            "message_status",
            {
                "up_to_position": up_to_position,
                "status": "read",
                "reader_id": user_id,
            },
            room=f"conv_{conversation_id}",
            skip_sid=request.sid,
        )
        return {"ok": True}