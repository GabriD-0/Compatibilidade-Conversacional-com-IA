# TODO: Reavaliar preprocessamento

def preprocessar(texto: str) -> list[str]:
    """Normaliza e tokeniza o texto. Stub: lower + split."""
    if not texto or not isinstance(texto, str):
        return []
    return texto.lower().strip().split()
