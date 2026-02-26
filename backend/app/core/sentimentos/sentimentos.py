# TODO: Reavaliar sentimentos

def analisar_sentimentos(mensagens: list[dict]) -> dict:
    """Retorna métricas de sentimento por mensagem e agregadas. Stub."""
    # mensagens: [{"autor": str, "texto": str}, ...]
    return {
        "polaridade_media": 0.2,
        "por_mensagem": [{"polaridade": 0.0} for _ in mensagens],
    }
