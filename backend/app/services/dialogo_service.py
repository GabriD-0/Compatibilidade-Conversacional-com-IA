from datetime import datetime
from app import db
from app.models import Dialogo, Mensagem, Analise, Metricas
from app.core import preprocessar, calcular_lsm, analisar_sentimentos, extrair_sinais, agregar, gerar_explicabilidade

# TODO: Reavaliar dialogo_service


def _mensagens_por_autor(mensagens: list[dict]) -> dict[str, list[str]]:
    """Agrupa textos pré-processados por autor."""
    from collections import defaultdict
    por_autor = defaultdict(list)
    for m in mensagens:
        autor = m.get("autor", "").strip() or "desconhecido"
        texto = m.get("texto", "") or ""
        tokens = preprocessar(texto)
        if tokens:
            por_autor[autor].extend(tokens)
    return dict(por_autor)


def criar_e_analisar(mensagens: list[dict]) -> tuple[Dialogo, Analise]:
    """Persiste o diálogo, executa o motor de IA e persiste score + métricas. Retorna (dialogo, analise)."""
    dialogo = Dialogo()
    db.session.add(dialogo)
    db.session.flush()

    for m in mensagens:
        ts = m.get("timestamp")
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                ts = datetime.utcnow()
        elif not ts:
            ts = datetime.utcnow()
        msg = Mensagem(
            dialogo_id=dialogo.id,
            autor=(m.get("autor") or "").strip() or "participante",
            texto=(m.get("texto") or "").strip(),
            timestamp=ts,
        )
        db.session.add(msg)

    db.session.flush()

    # Preparar dados para o motor
    lista_msg = [
        {"autor": msg.autor, "texto": msg.texto, "timestamp": msg.timestamp}
        for msg in dialogo.mensagens.order_by(Mensagem.timestamp)
    ]
    textos_por_autor = _mensagens_por_autor(lista_msg)

    lsm = calcular_lsm(textos_por_autor)
    metricas_sent = analisar_sentimentos(lista_msg)
    metricas_comp = extrair_sinais(lista_msg)
    score_final = agregar(lsm, metricas_sent, metricas_comp)
    explicabilidade_list = gerar_explicabilidade(
        score_final, lsm, metricas_sent, metricas_comp
    )

    analise = Analise(
        dialogo_id=dialogo.id,
        score_final=score_final,
        versao=dialogo.versao_calculo,
    )
    db.session.add(analise)
    db.session.flush()

    metricas = Metricas(
        analise_id=analise.id,
        lsm=lsm,
        metricas_sentimento=metricas_sent,
        metricas_comportamentais=metricas_comp,
        explicabilidade=explicabilidade_list,
    )
    db.session.add(metricas)
    db.session.commit()
    return dialogo, analise


def obter_dialogo_por_id(dialogo_id: int) -> Dialogo | None:
    """Retorna o diálogo por id ou None."""
    return db.session.get(Dialogo, dialogo_id)


def listar_dialogos(limit: int = 50, offset: int = 0) -> list[Dialogo]:
    """Lista diálogos com paginação."""
    return (
        Dialogo.query
        .order_by(Dialogo.data_criacao.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def obter_score_e_metricas(dialogo_id: int) -> dict | None:
    """Retorna score, métricas e explicabilidade para o diálogo ou None."""
    dialogo = obter_dialogo_por_id(dialogo_id)
    if not dialogo or not dialogo.analises:
        return None
    analise = dialogo.analises.order_by(Analise.data_calculo.desc()).first()
    if not analise or not analise.metricas:
        return None
    m = analise.metricas
    return {
        "score": analise.score_final,
        "metricas": {
            "lsm": m.lsm,
            "sentimento": m.metricas_sentimento,
            "comportamentais": m.metricas_comportamentais,
        },
        "explicabilidade": m.explicabilidade or [],
        "data_calculo": analise.data_calculo.isoformat() if analise.data_calculo else None,
    }
