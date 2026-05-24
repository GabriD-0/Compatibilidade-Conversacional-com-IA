import pytest
from datetime import datetime, timezone
from app.core.lsm.lsm import calculate_lsm, category_lsm, count_categories
from app.core.preprocessing import PreparedMessage


def prepared_message(sender_id, canonical_tokens):
    return PreparedMessage(
        id=None,
        position=0,
        sender_id=sender_id,
        content=" ".join(canonical_tokens),
        sent_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        normalized_content=" ".join(canonical_tokens),
        tokens=canonical_tokens,
        canonical_tokens=canonical_tokens,
        word_count=len(canonical_tokens),
        char_count=len(" ".join(canonical_tokens)),
    )


@pytest.mark.unit
def test_category_lsm_returns_none_when_category_is_absent_for_both_participants():
    assert category_lsm(0, 0) is None


@pytest.mark.unit
def test_category_lsm_scores_equal_ratios_as_perfect_match():
    assert category_lsm(0.2, 0.2) == 1.0


@pytest.mark.unit
def test_category_lsm_scores_different_ratios_lower():
    assert category_lsm(0.2, 0.0) < 0.01


@pytest.mark.unit
def test_count_categories_counts_function_words():
    total, counts = count_categories(
        [prepared_message(1, ["eu", "voce", "o", "de", "nunca", "banana"])]
    )

    assert total == 6
    assert counts["pronomes"] == 2
    assert counts["artigos"] == 1
    assert counts["preposicoes"] == 1
    assert counts["negacoes"] == 1
    assert counts["conjuncoes"] == 0


@pytest.mark.unit
def test_calculate_lsm_scores_identical_function_word_usage_as_high():
    messages = [
        prepared_message(1, ["eu", "de", "o", "nao"]),
        prepared_message(2, ["eu", "de", "o", "nao"]),
    ]

    metrics = calculate_lsm(messages, (1, 2))

    assert metrics["score"] == 100.0
    assert metrics["active_categories"] == 4
    assert metrics["category_scores"]["pronomes"] == 100.0
    assert metrics["participants"]["1"]["token_count"] == 4
    assert metrics["participants"]["2"]["category_counts"]["negacoes"] == 1


@pytest.mark.unit
def test_calculate_lsm_uses_neutral_score_when_no_categories_are_active():
    messages = [prepared_message(1, ["banana"]), prepared_message(2, ["abacaxi"])]

    metrics = calculate_lsm(messages, (1, 2))

    assert metrics["score"] == 50.0
    assert metrics["active_categories"] == 0
    assert all(score is None for score in metrics["category_scores"].values())
