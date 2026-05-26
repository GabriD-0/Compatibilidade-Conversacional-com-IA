import pytest
from datetime import datetime, timezone
from types import SimpleNamespace
from app.services.dashboard import build_dashboard_payload


def dt(day: int, hour: int = 12) -> datetime:
    return datetime(2026, 1, day, hour, tzinfo=timezone.utc)


def participant(name: str):
    return SimpleNamespace(name=name)


def conversation(
    id: int,
    *,
    a: str = "Ana",
    b: str = "Bruno",
    message_count: int = 0,
    created_at: datetime | None = None,
    last_message_at: datetime | None = None,
):
    return SimpleNamespace(
        id=id,
        participant_a_id=id * 10 + 1,
        participant_b_id=id * 10 + 2,
        participant_a=participant(a),
        participant_b=participant(b),
        message_count=message_count,
        created_at=created_at or dt(1),
        last_message_at=last_message_at,
    )


def metrics(
    *,
    lsm: float,
    sentiment: float,
    behavioral: float,
    turn_balance: float,
    response_speed: float,
    avg_response_seconds: float = 120,
    avg_words: float = 14,
    category_scores: dict | None = None,
    sentiment_messages: list[dict] | None = None,
):
    return {
        "aggregate": {
            "components": {
                "lsm": lsm,
                "sentiment": sentiment,
                "behavioral": behavioral,
            }
        },
        "behavioral": {
            "turn_balance": turn_balance,
            "response_speed": response_speed,
            "conversation": {
                "average_response_time_seconds": avg_response_seconds,
                "average_message_length_words": avg_words,
            },
        },
        "lsm": {"category_scores": category_scores or {"pronomes": 80, "artigos": None}},
        "sentiment": {"messages": sentiment_messages or []},
    }


def analysis(
    id: int,
    conversation_id: int,
    *,
    score: float,
    classification: str,
    computed_at: datetime,
    message_count: int = 10,
    analysis_metrics: dict | None = None,
):
    return SimpleNamespace(
        id=id,
        conversation_id=conversation_id,
        score=score,
        classification=classification,
        computed_at=computed_at,
        message_count=message_count,
        metrics=analysis_metrics
        or metrics(
            lsm=score,
            sentiment=score,
            behavioral=score,
            turn_balance=score,
            response_speed=score,
        ),
    )


@pytest.mark.unit
def test_dashboard_stats_and_score_distribution_use_latest_analyses():
    conversations = [
        conversation(1, message_count=8, created_at=dt(1), last_message_at=dt(8)),
        conversation(2, message_count=4, created_at=dt(2), last_message_at=dt(6)),
        conversation(3, message_count=0, created_at=dt(8)),
    ]
    analyses = [
        analysis(1, 1, score=80, classification="high", computed_at=dt(7)),
        analysis(2, 1, score=90, classification="high", computed_at=dt(8)),
        analysis(3, 2, score=70, classification="mid", computed_at=dt(6)),
        analysis(4, 2, score=65, classification="mid", computed_at=dt(7)),
    ]

    payload = build_dashboard_payload(
        login_id=11,
        conversations=conversations,
        analyses=analyses,
        now=dt(8),
    )

    assert payload["stats"]["average_score"] == {"value": 77.5, "delta": 2.5}
    assert payload["stats"]["conversations"]["value"] == 3
    assert payload["stats"]["active_pairs"]["value"] == 2
    assert payload["stats"]["analyses_today"]["value"] == 1
    assert payload["score_distribution"] == [
        {"range": "0-20", "count": 0},
        {"range": "21-40", "count": 0},
        {"range": "41-60", "count": 0},
        {"range": "61-80", "count": 1},
        {"range": "81-100", "count": 1},
    ]
    assert payload["classification_distribution"] == [
        {"key": "high", "label": "Alta (80+)", "value": 1},
        {"key": "mid", "label": "Media (60-79)", "value": 1},
        {"key": "low", "label": "Baixa (<60)", "value": 0},
    ]


@pytest.mark.unit
def test_dashboard_score_distribution_includes_zero_score():
    payload = build_dashboard_payload(
        login_id=11,
        conversations=[conversation(1)],
        analyses=[analysis(1, 1, score=0, classification="low", computed_at=dt(8))],
        now=dt(8),
    )

    assert payload["score_distribution"][0] == {"range": "0-20", "count": 1}


@pytest.mark.unit
def test_dashboard_weekly_scores_count_daily_analysis_and_message_activity():
    conversations = [
        conversation(1, message_count=2, last_message_at=dt(8)),
        conversation(2, message_count=3, last_message_at=dt(7)),
    ]
    analyses = [
        analysis(1, 1, score=90, classification="high", computed_at=dt(8)),
        analysis(2, 2, score=70, classification="mid", computed_at=dt(8)),
    ]

    payload = build_dashboard_payload(
        login_id=11,
        conversations=conversations,
        analyses=analyses,
        now=dt(8),
    )

    today = payload["weekly_scores"][-1]
    assert today["score"] == 80.0
    assert today["conversations"] == 1


@pytest.mark.unit
def test_dashboard_analyses_today_uses_sao_paulo_calendar_day():
    payload = build_dashboard_payload(
        login_id=11,
        conversations=[conversation(1)],
        analyses=[
            analysis(1, 1, score=90, classification="high", computed_at=datetime(2026, 1, 8, 1, tzinfo=timezone.utc)),
            analysis(2, 1, score=70, classification="mid", computed_at=datetime(2026, 1, 7, 1, tzinfo=timezone.utc)),
        ],
        now=datetime(2026, 1, 8, 2, tzinfo=timezone.utc),
    )

    assert payload["stats"]["analyses_today"] == {"value": 1, "delta": 0}


@pytest.mark.unit
def test_dashboard_recent_activity_uses_match_name_for_logged_user():
    payload = build_dashboard_payload(
        login_id=11,
        conversations=[conversation(1, a="Ana", b="Bruno")],
        analyses=[analysis(1, 1, score=90, classification="high", computed_at=dt(8))],
        now=dt(8),
    )

    assert payload["recent_activity"][0]["pair"] == "Bruno"


@pytest.mark.unit
def test_dashboard_top_pairs_are_ranked_and_have_score_trends():
    conversations = [
        conversation(1, a="Ana", b="Bruno"),
        conversation(2, a="Caio", b="Dina"),
    ]
    analyses = [
        analysis(1, 1, score=75, classification="mid", computed_at=dt(6)),
        analysis(2, 1, score=92, classification="high", computed_at=dt(8)),
        analysis(3, 2, score=81, classification="high", computed_at=dt(6)),
        analysis(4, 2, score=70, classification="mid", computed_at=dt(8)),
    ]

    payload = build_dashboard_payload(
        login_id=1,
        conversations=conversations,
        analyses=analyses,
        now=dt(8),
    )

    assert payload["top_pairs"][0] == {
        "conversation_id": 1,
        "a": "Ana",
        "b": "Bruno",
        "score": 92,
        "trend": "up",
    }
    assert payload["top_pairs"][1]["trend"] == "down"


@pytest.mark.unit
def test_dashboard_emotional_convergence_includes_selectable_conversations_and_lsm_uses_focus():
    conversations = [
        conversation(1, a="Ana", b="Bruno"),
        conversation(2, a="Caio", b="Dina"),
    ]
    focus_metrics = metrics(
        lsm=88,
        sentiment=74,
        behavioral=91,
        turn_balance=83,
        response_speed=76,
        category_scores={"pronomes": 82, "artigos": None, "preposicoes": 64},
        sentiment_messages=[
            {"position": 0, "sender_id": 11, "polarity": 0.4},
            {"position": 1, "sender_id": 12, "polarity": -0.2},
            {"position": 2, "sender_id": 11, "polarity": 0.7},
        ],
    )
    analyses = [
        analysis(1, 1, score=88, classification="high", computed_at=dt(7)),
        analysis(2, 1, score=91, classification="high", computed_at=dt(8), analysis_metrics=focus_metrics),
        analysis(3, 2, score=55, classification="low", computed_at=dt(6)),
    ]

    payload = build_dashboard_payload(
        login_id=11,
        conversations=conversations,
        analyses=analyses,
        now=dt(8),
    )

    assert payload["emotional_convergence"] == [
        {
            "conversation_id": 1,
            "label": "Bruno",
            "person_a": "Eu",
            "person_b": "Bruno",
            "points": [
                {"msg": 1, "person_a": 0.4, "person_b": None},
                {"msg": 2, "person_a": 0.4, "person_b": -0.2},
                {"msg": 3, "person_a": 0.7, "person_b": -0.2},
            ],
        }
    ]
    assert payload["lsm_categories"] == [
        {"category": "Pronomes", "similarity": 81.0},
        {"category": "Preposicoes", "similarity": 64.0},
    ]
    assert payload["behavioral_signs"][0]["pair"] == "Bruno"


@pytest.mark.unit
def test_dashboard_profile_uses_derived_engagement_reciprocity_and_fluency():
    conversations = [conversation(1), conversation(2)]
    analyses = [
        analysis(
            1,
            1,
            score=80,
            classification="high",
            computed_at=dt(8),
            message_count=10,
            analysis_metrics=metrics(
                lsm=90,
                sentiment=70,
                behavioral=60,
                turn_balance=80,
                response_speed=100,
            ),
        ),
        analysis(
            2,
            2,
            score=60,
            classification="mid",
            computed_at=dt(8),
            message_count=5,
            analysis_metrics=metrics(
                lsm=70,
                sentiment=50,
                behavioral=40,
                turn_balance=60,
                response_speed=80,
            ),
        ),
    ]

    payload = build_dashboard_payload(
        login_id=1,
        conversations=conversations,
        analyses=analyses,
        now=dt(8),
    )

    assert payload["profile"] == [
        {"metric": "LSM", "value": 80.0, "fullMark": 100},
        {"metric": "Emocao", "value": 60.0, "fullMark": 100},
        {"metric": "Comportamento", "value": 50.0, "fullMark": 100},
        {"metric": "Engajamento", "value": 75.0, "fullMark": 100},
        {"metric": "Reciprocidade", "value": 70.0, "fullMark": 100},
        {"metric": "Fluidez", "value": 90.0, "fullMark": 100},
    ]


@pytest.mark.unit
def test_dashboard_empty_state_keeps_stable_payload_shape():
    payload = build_dashboard_payload(login_id=1, conversations=[], analyses=[], now=dt(8))

    assert payload["stats"]["average_score"] == {"value": None, "delta": None}
    assert payload["stats"]["conversations"] == {"value": 0, "delta": 0}
    assert payload["profile"] == []
    assert payload["top_pairs"] == []
    assert payload["recent_activity"] == []
    assert payload["emotional_convergence"] == []
    assert payload["lsm_categories"] == []
    assert payload["behavioral_signs"] == []
    assert payload["scatter"] == []
