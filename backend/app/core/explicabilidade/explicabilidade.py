# TODO: Reavaliar explicabilidade

def gerar_explicabilidade(
    score: float,
    lsm: float,
    metricas_sentimento: dict,
    metricas_comportamentais: dict,
) -> list[str]:
    """Retorna lista de frases explicando os fatores. Stub."""
    explicacoes = []
    if lsm >= 0.7:
        explicacoes.append("Alto alinhamento de estilo linguístico entre os participantes.")
    elif lsm >= 0.4:
        explicacoes.append("Alinhamento moderado de estilo linguístico.")
    else:
        explicacoes.append("Estilo linguístico com menor convergência.")

    pol = metricas_sentimento.get("polaridade_media", 0)
    if pol is not None and pol > 0.1:
        explicacoes.append("Convergência emocional positiva no diálogo.")
    elif pol is not None and pol < -0.1:
        explicacoes.append("Tom emocional mais negativo no diálogo.")
    else:
        explicacoes.append("Tom emocional neutro.")

    eq = metricas_comportamentais.get("equilibrio_turnos")
    if eq is not None and eq >= 0.7:
        explicacoes.append("Bom equilíbrio de participação entre os participantes.")
    else:
        explicacoes.append("Participação com algum desequilíbrio de turnos.")

    return explicacoes
