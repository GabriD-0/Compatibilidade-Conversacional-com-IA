import logging
from __future__ import annotations
from datetime import datetime, timezone
from app.core.agregation import aggregate_metrics
from app.core.behavioral_signs import calculate_behavioral_signs
from app.core.explicability import build_explanation
from app.core.lsm import calculate_lsm
from app.core.preprocessing import prepare_messages
from app.core.sentiments import analyze_sentiments
from app.errors import ApiError
from app.extensions import db
from app.models import Conversation, ConversationAnalysis, Message
from app.services.conversation_service import get_conversation

log = logging.getLogger(__name__)

ANALYSIS_VERSION = "compatibility-hf-sentiment-v1"
MAX_MESSAGES_FOR_ANALYSIS = 1000
LOW_CONFIDENCE_MESSAGE_COUNT = 6


def analyze_conversation(login_id: int, conversation_id: int) -> dict:
    conversation = get_conversation(login_id, conversation_id)
    analysis = compute_and_persist_analysis(conversation)
    return serialize_analysis(analysis)


def get_latest_conversation_analysis(login_id: int, conversation_id: int) -> dict:
    conversation = get_conversation(login_id, conversation_id)
    analysis = get_latest_analysis_for_conversation(conversation.id)
    if analysis is None:
        raise ApiError("Analise ainda nao foi calculada.", code="analysis_not_found", status_code=404)
    return serialize_analysis(analysis)


def get_latest_analysis_for_conversation(conversation_id: int) -> ConversationAnalysis | None:
    return (
        ConversationAnalysis.query.filter_by(conversation_id=conversation_id)
        .order_by(ConversationAnalysis.computed_at.desc(), ConversationAnalysis.id.desc())
        .first()
    )


def auto_analyze_conversation(conversation_id: int) -> dict | None:
    conversation = db.session.get(Conversation, conversation_id)
    if conversation is None or not _has_messages_from_both_participants(conversation):
        return None

    analysis = compute_and_persist_analysis(conversation)
    return serialize_analysis(analysis)


def compute_and_persist_analysis(conversation: Conversation) -> ConversationAnalysis:
    _validate_conversation_header(conversation)

    if conversation.message_count > MAX_MESSAGES_FOR_ANALYSIS:
        raise ApiError(
            f"Conversa excede o limite de {MAX_MESSAGES_FOR_ANALYSIS} mensagens para analise.",
            code="analysis_too_large",
            status_code=413,
        )

    messages = (
        Message.query.filter_by(conversation_id=conversation.id)
        .order_by(Message.position)
        .all()
    )

    if len(messages) > MAX_MESSAGES_FOR_ANALYSIS:
        raise ApiError(
            f"Conversa excede o limite de {MAX_MESSAGES_FOR_ANALYSIS} mensagens para analise.",
            code="analysis_too_large",
            status_code=413,
        )

    participant_ids = (conversation.participant_a_id, conversation.participant_b_id)
    _validate_message_set(messages, participant_ids)

    try:
        prepared_messages = prepare_messages(messages)
    except ValueError as exc:
        raise ApiError(str(exc), code="invalid_analysis_data", status_code=422) from exc

    warnings = _build_warnings(prepared_messages, participant_ids)

    lsm_metrics = calculate_lsm(prepared_messages, participant_ids)
    try:
        sentiment_metrics = analyze_sentiments(prepared_messages, participant_ids)
    except RuntimeError as exc:
        raise ApiError(
            str(exc),
            code="sentiment_analyzer_unavailable",
            status_code=503,
        ) from exc
    behavioral_metrics = calculate_behavioral_signs(prepared_messages, participant_ids)

    if lsm_metrics.get("active_categories", 0) < 3:
        warnings.append(
            {
                "code": "low_lsm_evidence",
                "message": "Poucas categorias de palavras-funcao apareceram na conversa.",
            }
        )

    aggregate = aggregate_metrics(
        lsm_metrics=lsm_metrics,
        sentiment_metrics=sentiment_metrics,
        behavioral_metrics=behavioral_metrics,
        warnings=warnings,
    )
    explanation = build_explanation(
        aggregate=aggregate,
        lsm_metrics=lsm_metrics,
        sentiment_metrics=sentiment_metrics,
        behavioral_metrics=behavioral_metrics,
    )

    metrics = {
        "lsm": lsm_metrics,
        "sentiment": sentiment_metrics,
        "behavioral": behavioral_metrics,
        "aggregate": aggregate,
        "warnings": warnings,
    }

    analysis = ConversationAnalysis(
        conversation_id=conversation.id,
        score=aggregate["score"],
        classification=aggregate["classification"],
        metrics=metrics,
        explanation=explanation,
        analysis_version=ANALYSIS_VERSION,
        message_count_snapshot=len(prepared_messages),
        last_message_at_snapshot=conversation.last_message_at,
        computed_at=datetime.now(timezone.utc),
    )

    db.session.add(analysis)
    db.session.commit()
    log.info("Analise calculada: conv=%s score=%s", conversation.id, analysis.score)
    return analysis


def serialize_analysis(analysis: ConversationAnalysis) -> dict:
    metrics = analysis.metrics or {}
    computed_at = analysis.computed_at.isoformat() if analysis.computed_at else None
    last_message_at = (
        analysis.last_message_at_snapshot.isoformat()
        if analysis.last_message_at_snapshot
        else None
    )

    return {
        "id": analysis.id,
        "conversation_id": analysis.conversation_id,
        "score": round(float(analysis.score), 2),
        "classification": analysis.classification,
        "metrics": metrics,
        "explanation": analysis.explanation,
        "warnings": metrics.get("warnings", []),
        "analysis_version": analysis.analysis_version,
        "message_count": analysis.message_count_snapshot,
        "last_message_at": last_message_at,
        "computed_at": computed_at,
    }


def _validate_conversation_header(conversation: Conversation) -> None:
    if conversation.participant_b_id is None:
        raise ApiError(
            "A conversa precisa ter dois participantes para ser analisada.",
            code="analysis_not_enough_data",
        )


def _validate_message_set(messages: list[Message], participant_ids: tuple[int, int]) -> None:
    if not messages:
        raise ApiError(
            "A conversa ainda nao possui mensagens suficientes para analise.",
            code="analysis_not_enough_data",
        )

    senders = {message.sender_id for message in messages}
    if participant_ids[0] not in senders or participant_ids[1] not in senders:
        raise ApiError(
            "A analise exige mensagens dos dois participantes.",
            code="analysis_not_enough_data",
        )

    unexpected_senders = senders.difference(participant_ids)
    if unexpected_senders:
        raise ApiError(
            "A conversa possui mensagens de participantes invalidos.",
            code="invalid_analysis_data",
            status_code=422,
        )


def _build_warnings(messages: list, participant_ids: tuple[int, int]) -> list[dict]:
    warnings: list[dict] = []
    if len(messages) < LOW_CONFIDENCE_MESSAGE_COUNT:
        warnings.append(
            {
                "code": "low_message_count",
                "message": "Conversa pequena; o score tem baixa confianca.",
            }
        )

    for participant_id in participant_ids:
        participant_message_count = len(
            [message for message in messages if message.sender_id == participant_id]
        )
        if participant_message_count < 3:
            warnings.append(
                {
                    "code": "low_participant_message_count",
                    "participant_id": participant_id,
                    "message": "Participante tem poucas mensagens para uma analise robusta.",
                }
            )

    return warnings


def _has_messages_from_both_participants(conversation: Conversation) -> bool:
    if conversation.participant_b_id is None:
        return False

    participant_ids = (conversation.participant_a_id, conversation.participant_b_id)
    rows = (
        db.session.query(Message.sender_id)
        .filter(
            Message.conversation_id == conversation.id,
            Message.sender_id.in_(participant_ids),
        )
        .distinct()
        .all()
    )
    return {row[0] for row in rows} == set(participant_ids)
