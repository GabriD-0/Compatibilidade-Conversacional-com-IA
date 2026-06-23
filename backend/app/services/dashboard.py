from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import mean
from typing import Iterable, Any
from sqlalchemy import or_
from app.models import Conversation, ConversationAnalysis

WEEKDAY_LABELS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
APP_TIMEZONE = timezone(timedelta(hours=-3), "America/Sao_Paulo")

SCORE_BUCKETS = (
    (0, 20, "0-20"),
    (21, 40, "21-40"),
    (41, 60, "41-60"),
    (61, 80, "61-80"),
    (81, 100, "81-100"),
)

CLASSIFICATION_LABELS = {
    "high": "Alta (80+)",
    "mid": "Media (60-79)",
    "low": "Baixa (<60)",
}

CATEGORY_LABELS = {
    "pronomes": "Pronomes",
    "artigos": "Artigos",
    "preposicoes": "Preposicoes",
    "conjuncoes": "Conjuncoes",
    "negacoes": "Negacoes",
    "auxiliares": "Auxiliares",
    "adverbios_funcionais": "Adverbios",
    "quantificadores": "Quantificadores",
}


def get_dashboard_summary(login_id: int) -> dict:
    conversations = (
        Conversation.query.filter(
            or_(
                Conversation.participant_a_id == login_id,
                Conversation.participant_b_id == login_id,
            )
        )
        .all()
    )
    conversation_ids = [conversation.id for conversation in conversations]

    analyses = []
    if conversation_ids:
        analyses = ConversationAnalysis.query.filter(
            ConversationAnalysis.conversation_id.in_(conversation_ids)
        ).all()

    return build_dashboard_payload(
        login_id=login_id,
        conversations=conversations,
        analyses=analyses,
        now=datetime.now(timezone.utc),
    )


def build_dashboard_payload(*, login_id: int | None = None, conversations: Iterable[Any], analyses: Iterable[Any], now: datetime | None = None) -> dict:
    current_time = as_utc(now or datetime.now(timezone.utc))
    conversation_list = list(conversations)
    analysis_list = list(analyses)
    conversation_by_id = {conversation.id: conversation for conversation in conversation_list}
    latest_by_conversation, previous_by_conversation = group_analyses(analysis_list)
    latest_analyses = list(latest_by_conversation.values())

    return {
        "stats": build_stats(
            conversations=conversation_list,
            analyses=analysis_list,
            latest_analyses=latest_analyses,
            previous_by_conversation=previous_by_conversation,
            now=current_time,
        ),
        "weekly_scores": build_weekly_scores(
            conversations=conversation_list,
            analyses=analysis_list,
            now=current_time,
        ),
        "profile": build_profile(latest_analyses),
        "score_distribution": build_score_distribution(latest_analyses),
        "classification_distribution": buildclassification_distribution(latest_analyses),
        "top_pairs": build_top_pairs(
            login_id=login_id,
            conversations=conversation_by_id,
            latest_by_conversation=latest_by_conversation,
            previous_by_conversation=previous_by_conversation,
        ),
        "recent_activity": build_recent_activity(
            login_id=login_id,
            conversations=conversation_list,
            latest_by_conversation=latest_by_conversation,
        ),
        "emotional_convergence": build_emotional_convergence(
            login_id=login_id,
            conversations=conversation_by_id,
            latest_analyses=latest_analyses,
        ),
        "lsm_categories": build_lsm_categories(latest_analyses),
        "behavioral_signs": build_behavioral_signs(
            login_id=login_id,
            conversations=conversation_by_id,
            latest_analyses=latest_analyses,
        ),
        "scatter": build_scatter(
            conversations=conversation_by_id,
            latest_analyses=latest_analyses,
        ),
    }


def group_analyses(analyses: Iterable[Any]) -> tuple[dict[int, Any], dict[int, Any]]:
    grouped: dict[int, list[Any]] = defaultdict(list)
    for analysis in analyses:
        grouped[int(analysis.conversation_id)].append(analysis)

    latest: dict[int, Any] = {}
    previous: dict[int, Any] = {}
    for conversation_id, items in grouped.items():
        ordered = sorted(
            items,
            key=lambda item: (as_utc(getattr(item, "computed_at", None)), int(getattr(item, "id", 0) or 0)),
            reverse=True,
        )
        latest[conversation_id] = ordered[0]
        if len(ordered) > 1:
            previous[conversation_id] = ordered[1]

    return latest, previous


def build_stats(*, conversations: list[Any], analyses: list[Any], latest_analyses: list[Any], previous_by_conversation: dict[int, Any], now: datetime) -> dict:
    today = now.astimezone(APP_TIMEZONE).date()
    yesterday = today - timedelta(days=1)
    recent_cutoff = now - timedelta(days=7)

    average_score = average(score(analysis) for analysis in latest_analyses)
    previous_average = average(score(analysis) for analysis in previous_by_conversation.values())
    score_delta = round_or_none(
        average_score - previous_average
        if average_score is not None and previous_average is not None
        else None,
        1,
    )

    analyses_today = len(
        [analysis for analysis in analyses if date_of(getattr(analysis, "computed_at", None), APP_TIMEZONE) == today]
    )
    analyses_yesterday = len(
        [analysis for analysis in analyses if date_of(getattr(analysis, "computed_at", None), APP_TIMEZONE) == yesterday]
    )

    return {
        "average_score": {
            "value": round_or_none(average_score, 1),
            "delta": score_delta,
        },
        "conversations": {
            "value": len(conversations),
            "delta": len(
                [
                    conversation
                    for conversation in conversations
                    if as_utc(getattr(conversation, "created_at", None)) >= recent_cutoff
                ]
            ),
        },
        "analyzed_pairs": {
            "value": len(latest_analyses),
            "delta": len(
                [
                    analysis
                    for analysis in latest_analyses
                    if as_utc(getattr(analysis, "computed_at", None)) >= recent_cutoff
                ]
            ),
        },
        "analyses_today": {
            "value": analyses_today,
            "delta": analyses_today - analyses_yesterday,
        },
    }


def build_weekly_scores(*, conversations: list[Any], analyses: list[Any], now: datetime) -> list[dict]:
    today = now.astimezone(APP_TIMEZONE).date()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    rows = []

    for day in days:
        day_analyses = [
            analysis for analysis in analyses if date_of(getattr(analysis, "computed_at", None), APP_TIMEZONE) == day
        ]
        day_conversations = [
            conversation
            for conversation in conversations
            if date_of(getattr(conversation, "last_message_at", None), APP_TIMEZONE) == day
        ]
        rows.append(
            {
                "day": WEEKDAY_LABELS[day.weekday()],
                "score": round_or_none(average(score(analysis) for analysis in day_analyses), 1),
                "conversations": len(day_conversations),
            }
        )

    return rows


def build_profile(latest_analyses: list[Any]) -> list[dict]:
    if not latest_analyses:
        return []

    max_messages = max(int(getattr(analysis, "message_count", 0) or 0) for analysis in latest_analyses)
    engagement_values = [
        (int(getattr(analysis, "message_count", 0) or 0) / max_messages) * 100
        for analysis in latest_analyses
        if max_messages > 0
    ]

    metrics = [
        ("LSM", average(metric_number(analysis, "aggregate", "components", "lsm") for analysis in latest_analyses)),
        ("Emocao", average(metric_number(analysis, "aggregate", "components", "sentiment") for analysis in latest_analyses)),
        ("Comportamento", average(metric_number(analysis, "aggregate", "components", "behavioral") for analysis in latest_analyses)),
        ("Engajamento", average(engagement_values)),
        ("Reciprocidade", average(metric_number(analysis, "behavioral", "turn_balance") for analysis in latest_analyses)),
        ("Fluidez", average(metric_number(analysis, "behavioral", "response_speed") for analysis in latest_analyses)),
    ]

    return [
        {"metric": label, "value": round_or_none(value, 1) or 0, "fullMark": 100}
        for label, value in metrics
    ]


def build_score_distribution(latest_analyses: list[Any]) -> list[dict]:
    rows = []
    for minimum, maximum, label in SCORE_BUCKETS:
        rows.append(
            {
                "range": label,
                "count": len(
                    [
                        analysis
                        for analysis in latest_analyses
                        if score_in_bucket(score(analysis), minimum, maximum)
                    ]
                ),
            }
        )
    return rows


def buildclassification_distribution(latest_analyses: list[Any]) -> list[dict]:
    rows = []
    for key in ("high", "mid", "low"):
        rows.append(
            {
                "key": key,
                "label": CLASSIFICATION_LABELS[key],
                "value": len(
                    [
                        analysis
                        for analysis in latest_analyses
                        if classification(analysis) == key
                    ]
                ),
            }
        )
    return rows


def build_top_pairs(
    *,
    login_id: int | None = None,
    conversations: dict[int, Any],
    latest_by_conversation: dict[int, Any],
    previous_by_conversation: dict[int, Any],
) -> list[dict]:
    ranked = sorted(
        latest_by_conversation.items(),
        key=lambda item: score(item[1]) or 0,
        reverse=True,
    )

    rows = []
    for conversation_id, analysis in ranked[:4]:
        conversation = conversations.get(conversation_id)
        if conversation is None:
            continue

        previous = previous_by_conversation.get(conversation_id)
        rows.append(
            {
                "conversation_id": conversation_id,
                "pair": match_label(conversation=conversation, login_id=login_id),
                "score": round(score(analysis) or 0),
                "trend": trend(analysis, previous),
            }
        )
    return rows


def build_recent_activity(*, login_id: int | None = None, conversations: list[Any], latest_by_conversation: dict[int, Any]) -> list[dict]:
    events = []
    for conversation in conversations:
        analysis = latest_by_conversation.get(int(conversation.id))
        analysis_at = as_utc(getattr(analysis, "computed_at", None)) if analysis else None
        last_message_at = as_utc(getattr(conversation, "last_message_at", None))
        created_at = as_utc(getattr(conversation, "created_at", None))

        if analysis is not None and analysis_at and analysis_at >= max(last_message_at, created_at):
            action = "Nova analise"
            occurred_at = analysis_at
        elif getattr(conversation, "last_message_at", None):
            action = "Nova mensagem"
            occurred_at = last_message_at
        else:
            action = "Conversa iniciada"
            occurred_at = created_at

        events.append(
            {
                "conversation_id": int(conversation.id),
                "pair": match_label(conversation=conversation, login_id=login_id),
                "action": action,
                "score": round(score(analysis)) if analysis is not None and score(analysis) is not None else None,
                "occurred_at": isoformat(occurred_at),
            }
        )

    return sorted(events, key=lambda item: item["occurred_at"] or "", reverse=True)[:4]


def build_emotional_convergence(*, login_id: int | None = None, conversations: dict[int, Any], latest_analyses: list[Any]) -> list[dict]:
    rows = []
    ordered_analyses = sorted(
        latest_analyses,
        key=lambda analysis: as_utc(getattr(analysis, "computed_at", None)),
        reverse=True,
    )

    for analysis in ordered_analyses:
        conversation = conversations.get(int(analysis.conversation_id))
        if conversation is None:
            continue

        points = build_emotional_points(conversation=conversation, analysis=analysis)
        if not points:
            continue

        person_a = display_participant_name(
            participant=getattr(conversation, "participant_a", None),
            participant_id=getattr(conversation, "participant_a_id", None),
            login_id=login_id,
        )
        person_b = display_participant_name(
            participant=getattr(conversation, "participant_b", None),
            participant_id=getattr(conversation, "participant_b_id", None),
            login_id=login_id,
        )
        rows.append(
            {
                "conversation_id": int(analysis.conversation_id),
                "label": emotional_conversation_label(conversation=conversation, login_id=login_id),
                "person_a": person_a,
                "person_b": person_b,
                "points": points,
            }
        )

    return rows


def build_emotional_points(*, conversation: Any, analysis: Any) -> list[dict]:
    sentiment_messages = metric_value(analysis, "sentiment", "messages")
    if not isinstance(sentiment_messages, list):
        return []

    participant_a_id = int(getattr(conversation, "participant_a_id", 0) or 0)
    participant_b_id = int(getattr(conversation, "participant_b_id", 0) or 0)
    last_a: float | None = None
    last_b: float | None = None
    rows = []

    ordered = sorted(
        sentiment_messages,
        key=lambda item: int(item.get("position", 0) or 0) if isinstance(item, dict) else 0,
    )
    for index, item in enumerate(ordered, start=1):
        if not isinstance(item, dict):
            continue
        sender_id = int(item.get("sender_id", 0) or 0)
        polarity = number(item.get("polarity"))
        if polarity is None:
            continue
        if sender_id == participant_a_id:
            last_a = polarity
        elif sender_id == participant_b_id:
            last_b = polarity
        rows.append({"msg": index, "person_a": last_a, "person_b": last_b})

    return rows


def build_lsm_categories(latest_analyses: list[Any]) -> list[dict]:
    grouped_scores: dict[str, list[float]] = defaultdict(list)

    for analysis in latest_analyses:
        scores = metric_value(analysis, "lsm", "category_scores")
        if not isinstance(scores, dict):
            continue

        for key, value in scores.items():
            score = number(value)
            if score is None:
                continue
            grouped_scores[str(key)].append(score)

    rows = []
    ordered_keys = [
        *[key for key in CATEGORY_LABELS if key in grouped_scores],
        *[key for key in grouped_scores if key not in CATEGORY_LABELS],
    ]
    for key in ordered_keys:
        rows.append(
            {
                "category": CATEGORY_LABELS.get(key, key.replace("_", " ").title()),
                "similarity": round(average(grouped_scores[key]) or 0, 2),
            }
        )
    return rows


def build_behavioral_signs(*, login_id: int | None = None, conversations: dict[int, Any], latest_analyses: list[Any]) -> list[dict]:
    ordered = sorted(
        latest_analyses,
        key=lambda analysis: as_utc(getattr(analysis, "computed_at", None)),
        reverse=True,
    )
    rows = []
    for analysis in ordered[:3]:
        conversation = conversations.get(int(analysis.conversation_id))
        if conversation is None:
            continue
        latency_seconds = metric_number(analysis, "behavioral", "conversation", "average_response_time_seconds")
        rows.append(
            {
                "conversation_id": int(analysis.conversation_id),
                "pair": match_label(conversation=conversation, login_id=login_id),
                "latency_minutes": round_or_none(latency_seconds / 60 if latency_seconds is not None else None, 1),
                "balance": round_or_none(metric_number(analysis, "behavioral", "turn_balance"), 1) or 0,
                "message_length_words": round_or_none(
                    metric_number(analysis, "behavioral", "conversation", "average_message_length_words"),
                    1,
                )
                or 0,
            }
        )
    return rows


def build_scatter(*, conversations: dict[int, Any], latest_analyses: list[Any]) -> list[dict]:
    rows = []
    for analysis in latest_analyses:
        conversation = conversations.get(int(analysis.conversation_id))
        if conversation is None:
            continue

        lsm = metric_number(analysis, "aggregate", "components", "lsm")
        sentiment = metric_number(analysis, "aggregate", "components", "sentiment")
        analysis_score = score(analysis)

        if lsm is None or sentiment is None or analysis_score is None:
            continue

        rows.append(
            {
                "conversation_id": int(analysis.conversation_id),
                "pair": pair_label(conversation),
                "lsm": round(lsm, 2),
                "sentiment": round(sentiment, 2),
                "score": round(analysis_score, 2),
            }
        )

    return sorted(rows, key=lambda item: item["score"], reverse=True)[:12]


def focus_analysis(latest_analyses: list[Any]) -> Any | None:
    if not latest_analyses:
        return None
    return max(latest_analyses, key=lambda analysis: as_utc(getattr(analysis, "computed_at", None)))


def trend(current: Any, previous: Any | None) -> str:
    current_score = score(current)
    previous_score = score(previous)
    if current_score is None or previous_score is None:
        return "flat"
    if current_score > previous_score:
        return "up"
    if current_score < previous_score:
        return "down"
    return "flat"


def classification(analysis: Any) -> str:
    raw = getattr(analysis, "classification", None)
    if raw in CLASSIFICATION_LABELS:
        return raw
    score = score(analysis) or 0
    if score >= 80:
        return "high"
    if score >= 60:
        return "mid"
    return "low"


def pair_label(conversation: Any) -> str:
    return f"{participant_name(getattr(conversation, 'participant_a', None))} & {participant_name(getattr(conversation, 'participant_b', None))}"


def participant_name(participant: Any) -> str:
    if participant is None:
        return "Pendente"
    return str(getattr(participant, "name", None) or "Participante")


def display_participant_name(*, participant: Any, participant_id: Any, login_id: int | None) -> str:
    if login_id is not None and int(participant_id or 0) == int(login_id):
        return "Eu"
    return participant_name(participant)


def emotional_conversation_label(*, conversation: Any, login_id: int | None) -> str:
    return match_label(conversation=conversation, login_id=login_id)


def match_label(*, conversation: Any, login_id: int | None) -> str:
    participant_a_id = int(getattr(conversation, "participant_a_id", 0) or 0)
    participant_b_id = int(getattr(conversation, "participant_b_id", 0) or 0)

    if login_id is not None and participant_a_id == int(login_id):
        return participant_name(getattr(conversation, "participant_b", None))
    if login_id is not None and participant_b_id == int(login_id):
        return participant_name(getattr(conversation, "participant_a", None))

    return pair_label(conversation)


def metric_number(analysis: Any, *path: str) -> float | None:
    return number(metric_value(analysis, *path))


def metric_value(analysis: Any, *path: str) -> Any:
    current = getattr(analysis, "metrics", None) or {}
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def score(analysis: Any | None) -> float | None:
    if analysis is None:
        return None
    return number(getattr(analysis, "score", None))


def score_in_bucket(score: float | None, minimum: int, maximum: int) -> bool:
    if score is None:
        return False
    if minimum == 0:
        return minimum <= score <= maximum
    return minimum - 1 < score <= maximum


def average(values: Iterable[float | int | None]) -> float | None:
    numeric = [number(value) for value in values]
    filtered = [value for value in numeric if value is not None]
    if not filtered:
        return None
    return float(mean(filtered))


def number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def round_or_none(value: float | None, digits: int = 2) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def date_of(value: Any, tz: timezone = timezone.utc) -> object | None:
    if value is None:
        return None
    return as_utc(value).astimezone(tz).date()


def as_utc(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    return datetime.min.replace(tzinfo=timezone.utc)


def isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    return as_utc(value).isoformat()
