def build_explanation(aggregate: dict, lsm_metrics: dict, sentiment_metrics: dict, behavioral_metrics: dict,) -> dict:
    """Constroi uma explicacao detalhada para a classificacao de compatibilidade."""

    components = aggregate["components"]
    factors = [
        explain_factor(
            key="lsm",
            label="Similaridade de estilo linguistico",
            score=components["lsm"],
            positive="Uso parecido de palavras-funcao entre os participantes.",
            negative="Uso diferente de palavras-funcao entre os participantes.",
        ),
        explain_factor(
            key="sentiment",
            label="Convergencia emocional",
            score=components["sentiment"],
            positive="Sentimentos estao alinhadas.",
            negative="Sentimentos variam bastante entre os participantes ou entre turnos.",
        ),
        explain_factor(
            key="behavioral",
            label="Sinais comportamentais",
            score=components["behavioral"],
            positive="Turnos, tamanhos de mensagem e respostas estao equilibrados.",
            negative="Ha desequilibrio em turnos, tamanho das mensagens ou tempo de resposta.",
        ),
    ]

    strongest = max(factors, key=lambda item: item["score"])
    weakest = min(factors, key=lambda item: item["score"])

    summary = summary_for_classification(aggregate["classification"], aggregate["score"])
    summary += f" Principal ponto forte: {strongest['label'].lower()}."

    if weakest["score"] < 60:
        summary += f" Ponto de atencao: {weakest['label'].lower()}."

    return {
        "summary": summary,
        "factors": factors,
        "details": {
            "lsm_active_categories": lsm_metrics.get("active_categories", 0),
            "sentiment_turn_convergence": sentiment_metrics.get("conversation", {}).get(
                "turn_convergence"
            ),
            "behavioral_turn_balance": behavioral_metrics.get("turn_balance"),
        },
    }


def explain_factor(key: str, label: str, score: float, positive: str, negative: str) -> dict:
    if score >= 75:
        impact = "positive"
        description = positive
    elif score >= 55:
        impact = "neutral"
        description = "O sinal contribui de forma moderada para o score."
    else:
        impact = "negative"
        description = negative

    return {
        "key": key,
        "label": label,
        "score": round(float(score), 2),
        "impact": impact,
        "description": description,
    }


def summary_for_classification(classification: str, score: float) -> str:
    if classification == "high":
        return f"Compatibilidade alta ({round(score)}%)."

    if classification == "mid":
        return f"Compatibilidade moderada ({round(score)}%)."

    return f"Compatibilidade baixa ({round(score)}%)."
