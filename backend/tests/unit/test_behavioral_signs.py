import pytest
from datetime import datetime, timedelta, timezone
from app.core.behavioral_signs.behavioral_signs import balance_score, calculate_behavioral_signs, calculate_response_times, mean_or_none, mean_or_zero, response_speed_score, round_or_none
from app.core.preprocessing import PreparedMessage


BASE_TIME = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


def prepared_message(sender_id, position, word_count=2, seconds=0):
    return PreparedMessage(
        id=position + 1,
        position=position,
        sender_id=sender_id,
        content="ola mundo",
        sent_at=BASE_TIME + timedelta(seconds=seconds),
        normalized_content="ola mundo",
        tokens=["ola", "mundo"][:word_count],
        canonical_tokens=["ola", "mundo"][:word_count],
        word_count=word_count,
        char_count=9,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(0, 0, 100.0), (0, 0, 50.0), (10, 10, 100.0), (5, 10, 50.0), (0, 10, 0.0)],
)
def test_balance_score(first, second, expected):
    neutral = first == 0 and second == 0 and expected == 50.0

    assert balance_score(first, second, neutral_when_empty=neutral) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        ([], 50.0),
        ([60], 100.0),
        ([30 * 60], 85.0),
        ([3 * 60 * 60], 65.0),
        ([12 * 60 * 60], 45.0),
        ([2 * 24 * 60 * 60], 25.0),
    ],
)
def test_response_speed_score_thresholds(seconds, expected):
    assert response_speed_score(seconds) == expected


@pytest.mark.unit
def test_calculate_response_times_uses_only_turn_changes_and_ignores_negative_deltas():
    messages = [
        prepared_message(1, 0, seconds=120),
        prepared_message(2, 1, seconds=60),
        prepared_message(2, 2, seconds=180),
        prepared_message(1, 3, seconds=300),
        prepared_message(3, 4, seconds=360),
    ]

    response_times = calculate_response_times(messages, (1, 2))

    assert response_times == {1: [120.0], 2: []}


@pytest.mark.unit
def test_calculate_behavioral_signs_scores_balanced_conversation():
    messages = [
        prepared_message(1, 0, seconds=0),
        prepared_message(2, 1, seconds=60),
        prepared_message(1, 2, seconds=120),
        prepared_message(2, 3, seconds=180),
    ]

    metrics = calculate_behavioral_signs(messages, (1, 2))

    assert metrics["score"] == 100.0
    assert metrics["turn_balance"] == 100.0
    assert metrics["length_balance"] == 100.0
    assert metrics["response_time_balance"] == 100.0
    assert metrics["response_speed"] == 100.0
    assert metrics["participants"]["1"]["message_count"] == 2
    assert metrics["participants"]["2"]["response_count"] == 2
    assert metrics["conversation"]["message_count"] == 4


@pytest.mark.unit
def test_mean_and_round_helpers_handle_empty_values():
    assert mean_or_none([]) is None
    assert mean_or_zero([]) == 0.0
    assert round_or_none(None) is None
    assert round_or_none(1.234) == 1.23
