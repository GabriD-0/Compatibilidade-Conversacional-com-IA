import logging
from datetime import datetime, timezone
from sqlalchemy import and_, or_, update
from app.errors import ApiError
from app.extensions import db
from app.models import Conversation, Login, Message

log = logging.getLogger(__name__)

_MAX_CONTENT = 4096
_MAX_LIMIT = 200
_MAX_PER_PAGE = 100

def create_conversation(login_id: int, data: dict) -> Conversation:
    participant_id = data.get("participant_id")
    if not participant_id or not isinstance(participant_id, int):
        raise ApiError("participant_id é obrigatório.", code="missing_participant_id")

    other = db.session.get(Login, participant_id)
    if other is None:
        raise ApiError("Usuário não encontrado.", code="user_not_found", status_code=404)

    if other.id == login_id:
        raise ApiError("Não é possível criar uma conversa consigo mesmo.", code="self_conversation")

    existing = Conversation.query.filter(
        or_(
            and_(
                Conversation.participant_a_id == login_id,
                Conversation.participant_b_id == other.id,
            ),
            and_(
                Conversation.participant_a_id == other.id,
                Conversation.participant_b_id == login_id,
            ),
        )
    ).first()

    if existing:
        raise ApiError("Conversa já existe entre esses usuários.", code="conversation_exists", status_code=409, details={"id": existing.id})

    conv = Conversation(participant_a_id=login_id, participant_b_id=other.id)
    db.session.add(conv)
    db.session.commit()
    return conv


def list_conversations(login_id: int, page: int = 1, per_page: int = 20):
    per_page = min(per_page, _MAX_PER_PAGE)
    page = max(page, 1)

    paginated = (
        Conversation.query.filter(
            or_(
                Conversation.participant_a_id == login_id,
                Conversation.participant_b_id == login_id,
            )
        )
        .order_by(Conversation.last_message_at.desc().nullslast())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return paginated.items, paginated.total


def get_conversation(login_id: int, conversation_id: int) -> Conversation:
    conv = db.session.get(Conversation, conversation_id)

    if conv is None or (conv.participant_a_id != login_id and conv.participant_b_id != login_id):
        raise ApiError("Conversa não encontrada.", code="not_found", status_code=404)

    return conv


def get_messages(login_id: int, conversation_id: int, after_position: int = 0, limit: int = 50) -> list:
    conv = get_conversation(login_id, conversation_id)
    limit = min(max(limit, 1), _MAX_LIMIT)

    return (
        Message.query.filter(
            Message.conversation_id == conv.id,
            Message.position >= after_position,
        )
        .order_by(Message.position)
        .limit(limit)
        .all()
    )


def delete_conversation(login_id: int, conversation_id: int) -> None:
    conv = get_conversation(login_id, conversation_id)
    db.session.delete(conv)
    db.session.commit()


def persist_message(conversation_id: int, sender_id: int, content: str) -> Message:
    """Insere uma mensagem atomicamente e atualiza o cabeçalho da conversa."""
    if not content or not content.strip():
        raise ApiError("Mensagem não pode estar vazia.", code="empty_content")

    if len(content) > _MAX_CONTENT:
        raise ApiError(f"Mensagem excede {_MAX_CONTENT} caracteres.", code="content_too_long")

    now = datetime.now(timezone.utc)

    # Incremento atômico: garante position único mesmo sob concorrência
    result = db.session.execute(
        update(Conversation)
        .where(Conversation.id == conversation_id)
        .values(
            message_count=Conversation.message_count + 1,
            last_message_at=now,
        )
        .returning(Conversation.message_count)
    )
    new_count = result.scalar_one()
    position = new_count - 1  # 0-based

    msg = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content.strip(),
        sent_at=now,
        position=position,
        status="sent",
    )
    db.session.add(msg)
    db.session.commit()

    log.info(
        "Mensagem persistida: conv=%s pos=%s sender=%s",
        conversation_id,
        position,
        sender_id,
    )
    return msg


def mark_read(conversation_id: int, reader_id: int, up_to_position: int) -> None:
    """Marca como lidas todas as mensagens do outro participante até a posição indicada."""
    db.session.execute(
        update(Message)
        .where(
            and_(
                Message.conversation_id == conversation_id,
                Message.sender_id != reader_id,
                Message.position <= up_to_position,
                Message.status != "read",
            )
        )
        .values(status="read")
    )
    db.session.commit()