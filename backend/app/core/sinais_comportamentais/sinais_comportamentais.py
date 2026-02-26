# TODO: Reavaliar sinais comportamentais

def extrair_sinais(mensagens: list[dict]) -> dict:
    """Retorna latência média, equilíbrio de turnos, comprimento médio. Stub."""
    # mensagens: [{"autor": str, "texto": str, "timestamp": str ou datetime}, ...]
    return {
        "latencia_media_segundos": 120.0,
        "equilibrio_turnos": 0.85,
        "comprimento_medio_caracteres": 45.0,
    }
