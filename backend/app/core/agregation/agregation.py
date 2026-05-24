DEFAULT_WEIGHTS = {
    "lsm": 0.40,
    "sentiment": 0.35,
    "behavioral": 0.25,
}


def aggregate_metrics(
    lsm_metrics: dict,
    sentiment_metrics: dict,
    behavioral_metrics: dict,
    warnings: list[dict] | None = None,
    weights: dict[str, float] | None = None,
) -> dict:

    selected_weights = weights or DEFAULT_WEIGHTS
    weighted_score = (
        selected_weights["lsm"] * float(lsm_metrics["score"])
        + selected_weights["sentiment"] * float(sentiment_metrics["score"])
        + selected_weights["behavioral"] * float(behavioral_metrics["score"])
    )
    score = round(max(0.0, min(100.0, weighted_score)), 2)

    return {
        "score": score,
        "classification": classify_score(score),
        "weights": selected_weights,
        "components": {
            "lsm": round(float(lsm_metrics["score"]), 2),
            "sentiment": round(float(sentiment_metrics["score"]), 2),
            "behavioral": round(float(behavioral_metrics["score"]), 2),
        },
        "warnings": warnings or [],
    }


def classify_score(score: float) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "mid"
    return "low"
