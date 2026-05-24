import pytest
from datetime import datetime, timezone
from types import SimpleNamespace
from app.errors import ApiError
from app.services.analysis import _build_warnings, _validate_conversation_header, _validate_message_set, serialize_analysis


@pytest.mark.unit
def test_validate_conversation_header_requires_second_participant():
    with pytest.raises(ApiError) as exc_info:
        _validate_conversation_header(SimpleNamespace(participant_b_id=None))

    assert exc_info.value.code == "analysis_not_enough_data"


@pytest.mark.unit
def test_validate_conversation_header_accepts_complete_conversation():
    _validate_conversation_header(SimpleNamespace(participant_b_id=2))


@pytest.mark.unit
def test_validate_message_set_requires_messages():
    with pytest.raises(ApiError) as exc_info:
        _validate_message_set([], (1, 2))

    assert exc_info.value.code == "analysis_not_enough_data"


@pytest.mark.unit
def test_validate_message_set_requires_both_participants():
    messages = [SimpleNamespace(sender_id=1)]

    with pytest.raises(ApiError) as exc_info:
        _validate_message_set(messages, (1, 2))

    assert exc_info.value.code == "analysis_not_enough_data"


@pytest.mark.unit
def test_validate_message_set_rejects_unexpected_senders():
    messages = [
        SimpleNamespace(sender_id=1),
        SimpleNamespace(sender_id=2),
        SimpleNamespace(sender_id=3),
    ]

    with pytest.raises(ApiError) as exc_info:
        _validate_message_set(messages, (1, 2))

    assert exc_info.value.code == "invalid_analysis_data"
    assert exc_info.value.status_code == 422


@pytest.mark.unit
def test_validate_message_set_accepts_messages_from_both_participants_only():
    messages = [SimpleNamespace(sender_id=1), SimpleNamespace(sender_id=2)]

    _validate_message_set(messages, (1, 2))


@pytest.mark.unit
def test_build_warnings_reports_small_conversations_and_low_participant_counts():
    messages = [SimpleNamespace(sender_id=1), SimpleNamespace(sender_id=2)]

    warnings = _build_warnings(messages, (1, 2))

    assert [warning["code"] for warning in warnings] == [
        "low_message_count",
        "low_participant_message_count",
        "low_participant_message_count",
    ]
    assert {warning.get("participant_id") for warning in warnings[1:]} == {1, 2}


@pytest.mark.unit
def test_serialize_analysis_formats_public_payload():
    computed_at = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    last_message_at = datetime(2026, 1, 1, 11, 30, tzinfo=timezone.utc)
    analysis = SimpleNamespace(
        id=7,
        conversation_id=3,
        score=75.126,
        classification="mid",
        metrics={"warnings": [{"code": "low_message_count"}]},
        explanation={"summary": "Resumo"},
        message_count=4,
        last_message_at=last_message_at,
        computed_at=computed_at,
    )

    assert serialize_analysis(analysis) == {
        "id": 7,
        "conversation_id": 3,
        "score": 75.13,
        "classification": "mid",
        "metrics": {"warnings": [{"code": "low_message_count"}]},
        "explanation": {"summary": "Resumo"},
        "warnings": [{"code": "low_message_count"}],
        "message_count": 4,
        "last_message_at": "2026-01-01T11:30:00+00:00",
        "computed_at": "2026-01-01T12:00:00+00:00",
    }


@pytest.mark.unit
def test_serialize_analysis_handles_missing_optional_dates_and_metrics():
    analysis = SimpleNamespace(
        id=1,
        conversation_id=2,
        score=10,
        classification="low",
        metrics=None,
        explanation={},
        message_count=0,
        last_message_at=None,
        computed_at=None,
    )

    payload = serialize_analysis(analysis)

    assert payload["metrics"] == {}
    assert payload["warnings"] == []
    assert payload["last_message_at"] is None
    assert payload["computed_at"] is None
