import pytest
from app.core.preprocessing import PreparedMessage
from app.core.sentiments.sentiments import SentimentAnalyzer, SentimentResult, analyze_sentiments, build_sentiment_metrics, canonical_model_label, label_from_polarity, normalize_pipeline_outputs


@pytest.mark.unit
def test_sentiment_result_to_dict_includes_optional_fields_only_when_present():
    minimal = SentimentResult(
        message_id=None,
        position=0,
        sender_id=1,
        label="neutral",
        polarity=0.0,
        intensity=0.0,
        evidence_count=1,
    )
    complete = SentimentResult(
        message_id=2,
        position=1,
        sender_id=1,
        label="positive",
        polarity=0.5,
        intensity=0.5,
        evidence_count=1,
        confidence=0.98,
        source_label="Positive",
    )

    assert "confidence" not in minimal.to_dict()
    assert "source_label" not in minimal.to_dict()
    assert complete.to_dict()["confidence"] == 0.98
    assert complete.to_dict()["source_label"] == "Positive"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("source", "canonical"),
    [
        ("LABEL_0", "Very Negative"),
        ("negative", "Negative"),
        ("Neutral", "Neutral"),
        ("very positive", "Very Positive"),
    ],
)
def test_canonical_model_label_accepts_known_aliases(source, canonical):
    assert canonical_model_label(source) == canonical


@pytest.mark.unit
def test_canonical_model_label_rejects_unknown_labels():
    with pytest.raises(RuntimeError, match="Rotulo de sentimento desconhecido"):
        canonical_model_label("unknown")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("polarity", "label"),
    [(0.15, "positive"), (0.149, "neutral"), (-0.15, "negative"), (-0.149, "neutral")],
)
def test_label_from_polarity_boundaries(polarity, label):
    assert label_from_polarity(polarity) == label


@pytest.mark.unit
def test_normalize_pipeline_outputs_accepts_single_dict():
    output = {"label": "Neutral", "score": 0.9}

    assert normalize_pipeline_outputs(output, expected_count=1) == [output]


@pytest.mark.unit
def test_normalize_pipeline_outputs_accepts_flat_list():
    outputs = [{"label": "Neutral", "score": 0.9}, {"label": "Positive", "score": 0.8}]

    assert normalize_pipeline_outputs(outputs, expected_count=2) == outputs


@pytest.mark.unit
def test_normalize_pipeline_outputs_selects_best_nested_result():
    outputs = [[{"label": "Negative", "score": 0.1}, {"label": "Positive", "score": 0.9}]]

    assert normalize_pipeline_outputs(outputs, expected_count=1) == [
        {"label": "Positive", "score": 0.9}
    ]


@pytest.mark.unit
def test_normalize_pipeline_outputs_rejects_unexpected_shapes():
    with pytest.raises(RuntimeError, match="Resposta invalida"):
        normalize_pipeline_outputs("invalid", expected_count=1)

    with pytest.raises(RuntimeError, match="Quantidade inesperada"):
        normalize_pipeline_outputs([{"label": "Neutral", "score": 0.9}], expected_count=2)


@pytest.mark.unit
def test_build_sentiment_metrics_scores_convergent_conversation():
    results = [
        SentimentResult(
            message_id=1,
            position=0,
            sender_id=1,
            label="positive",
            polarity=0.5,
            intensity=0.5,
            evidence_count=1,
        ),
        SentimentResult(
            message_id=2,
            position=1,
            sender_id=2,
            label="positive",
            polarity=0.5,
            intensity=0.5,
            evidence_count=1,
        ),
    ]

    metrics = build_sentiment_metrics(results, (1, 2), metadata={"provider": "fake"})

    assert metrics["score"] == 100.0
    assert metrics["provider"] == "fake"
    assert metrics["participants"]["1"]["distribution"] == {
        "positive": 1,
        "neutral": 0,
        "negative": 0,
    }
    assert metrics["conversation"]["turn_convergence"] == 100.0


@pytest.mark.unit
def test_build_sentiment_metrics_handles_empty_results():
    metrics = build_sentiment_metrics([], (1, 2))

    assert metrics["score"] == 80.0
    assert metrics["participants"]["1"]["message_count"] == 0
    assert metrics["conversation"]["average_polarity"] == 0.0
    assert metrics["conversation"]["turn_convergence"] == 50.0


@pytest.mark.unit
def test_analyze_sentiments_uses_injected_analyzer_without_loading_default_model():
    class FakeAnalyzer(SentimentAnalyzer):
        def analyze_messages(self, messages, participant_ids):
            return {
                "message_count": len(messages),
                "participant_ids": participant_ids,
                "provider": "fake",
            }

    messages = [
        PreparedMessage(
            id=1,
            position=0,
            sender_id=1,
            content="Ola",
            sent_at=None,
            normalized_content="ola",
            tokens=["ola"],
            canonical_tokens=["ola"],
            word_count=1,
            char_count=3,
        )
    ]

    assert analyze_sentiments(messages, (1, 2), analyzer=FakeAnalyzer()) == {
        "message_count": 1,
        "participant_ids": (1, 2),
        "provider": "fake",
    }
