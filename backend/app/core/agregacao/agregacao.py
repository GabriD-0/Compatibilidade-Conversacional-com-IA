# TODO: Reavaliar agregacao

def agregar(lsm: float, metricas_sentimento: dict, metricas_comportamentais: dict) -> float:
    w_lsm = 0.4
    w_sent = 0.35
    w_comp = 0.25
    # Normalizar polaridade (-1..1) -> (0..1): (x + 1) / 2
    pol = metricas_sentimento.get("polaridade_media", 0.0)
    sent_norm = (pol + 1) / 2.0 if pol is not None else 0.5
    comp_norm = metricas_comportamentais.get("equilibrio_turnos", 0.5) or 0.5
    score = w_lsm * lsm + w_sent * sent_norm + w_comp * comp_norm
    return round(min(1.0, max(0.0, score)), 4)
