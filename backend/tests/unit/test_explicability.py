import pytest
from app.core.explicability.explicability import build_explanation, explain_factor, summary_for_classification


@pytest.mark.unit
@pytest.mark.parametrize(
    ("classification", "score", "summary"),
    [
        ("high", 85, "Compatibilidade alta (85%)."),
        ("mid", 65, "Compatibilidade moderada (65%)."),
        ("low", 45, "Compatibilidade baixa (45%)."),
    ],
)
def test_summary_for_classification(classification, score, summary):
    assert summary_for_classification(classification, score) == summary


@pytest.mark.unit
@pytest.mark.parametrize(
    ("score", "impact", "description"),
    [
        (75, "positive", "positivo"),
        (55, "neutral", "moderada"),
        (54.99, "negative", "negativo"),
    ],
)
def test_explain_factor_uses_score_thresholds(score, impact, description):
    factor = explain_factor(
        key="factor",
        label="Fator",
        score=score,
        positive="Sinal positivo.",
        negative="Sinal negativo.",
    )

    assert factor["impact"] == impact
    assert description in factor["description"].lower()


@pytest.mark.unit
def test_build_explanation_identifies_strongest_and_weakest_factors():
    explanation = build_explanation(
        aggregate={
            "score": 58,
            "classification": "low",
            "components": {"lsm": 90, "sentiment": 50, "behavioral": 30},
        },
        lsm_metrics={"active_categories": 4},
        sentiment_metrics={"conversation": {"turn_convergence": 72}},
        behavioral_metrics={"turn_balance": 40},
    )

    assert explanation["summary"] == (
        "Compatibilidade baixa (58%). Principal ponto forte: "
        "similaridade de estilo linguistico. Ponto de atencao: sinais comportamentais."
    )
    assert [factor["key"] for factor in explanation["factors"]] == [
        "lsm",
        "sentiment",
        "behavioral",
    ]
    assert explanation["details"] == {
        "lsm_active_categories": 4,
        "sentiment_turn_convergence": 72,
        "behavioral_turn_balance": 40,
    }
