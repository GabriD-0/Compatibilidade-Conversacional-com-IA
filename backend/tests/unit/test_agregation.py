import pytest
from app.core.agregation import aggregate_metrics, classify_score


@pytest.mark.unit
@pytest.mark.parametrize(
    ("score", "classification"),
    [
        (100, "high"),
        (80, "high"),
        (79.99, "mid"),
        (60, "mid"),
        (59.99, "low"),
        (0, "low"),
    ],
)
def test_classify_score_boundaries(score, classification):
    assert classify_score(score) == classification


@pytest.mark.unit
def test_aggregate_metrics_applies_default_weights_and_preserves_warnings():
    aggregate = aggregate_metrics(
        lsm_metrics={"score": 80},
        sentiment_metrics={"score": 60},
        behavioral_metrics={"score": 40},
        warnings=[{"code": "low_message_count"}],
    )

    assert aggregate == {
        "score": 63.0,
        "classification": "mid",
        "weights": {"lsm": 0.40, "sentiment": 0.35, "behavioral": 0.25},
        "components": {"lsm": 80.0, "sentiment": 60.0, "behavioral": 40.0},
        "warnings": [{"code": "low_message_count"}],
    }


@pytest.mark.unit
def test_aggregate_metrics_clamps_score_to_valid_range():
    high = aggregate_metrics(
        lsm_metrics={"score": 200},
        sentiment_metrics={"score": 200},
        behavioral_metrics={"score": 200},
    )
    low = aggregate_metrics(
        lsm_metrics={"score": -50},
        sentiment_metrics={"score": -50},
        behavioral_metrics={"score": -50},
    )

    assert high["score"] == 100.0
    assert high["classification"] == "high"
    assert low["score"] == 0.0
    assert low["classification"] == "low"


@pytest.mark.unit
def test_aggregate_metrics_accepts_custom_weights():
    aggregate = aggregate_metrics(
        lsm_metrics={"score": 10},
        sentiment_metrics={"score": 50},
        behavioral_metrics={"score": 100},
        weights={"lsm": 0.0, "sentiment": 0.5, "behavioral": 0.5},
    )

    assert aggregate["score"] == 75.0
    assert aggregate["classification"] == "mid"
