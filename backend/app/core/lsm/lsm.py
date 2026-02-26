# TODO: Reavaliar lsm

def calcular_lsm(mensagens_por_autor: dict[str, list[str]]) -> float:
    """Retorna índice LSM entre dois autores. Stub: valor fixo."""
    # Esperado: {"autor1": ["msg1", "msg2"], "autor2": ["msg1", "msg2"]}
    if not mensagens_por_autor or len(mensagens_por_autor) < 2:
        return 0.0
    return 0.75
