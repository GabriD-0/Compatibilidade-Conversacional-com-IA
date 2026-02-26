from flask import Blueprint, request, jsonify
from app.models import Analise, Mensagem
from app.services.dialogo_service import criar_e_analisar, obter_dialogo_por_id, listar_dialogos, obter_score_e_metricas

# TODO: Reavaliar rotas

bp = Blueprint("dialogos", __name__)

def _validar_mensagens(data: dict) -> list[dict] | tuple[None, str]:
    """Valida payload de mensagens. Retorna (mensagens, None) ou (None, mensagem_erro)."""
    mensagens = data.get("mensagens")
    if not isinstance(mensagens, list):
        return None, "Campo 'mensagens' deve ser uma lista."
    if len(mensagens) < 2:
        return None, "É necessário pelo menos duas mensagens para analisar."
    for i, m in enumerate(mensagens):
        if not isinstance(m, dict):
            return None, f"Mensagem {i + 1} deve ser um objeto."
        if "texto" not in m or not str(m.get("texto", "")).strip():
            return None, f"Mensagem {i + 1} deve conter 'texto' não vazio."
        if "autor" not in m or not str(m.get("autor", "")).strip():
            return None, f"Mensagem {i + 1} deve conter 'autor' não vazio."
    return mensagens, None


@bp.route("/dialogos", methods=["POST"])
def post_dialogos():
    """Recebe diálogo (mensagens com autor e timestamp), persiste e analisa. Retorna id e status."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Corpo da requisição deve ser JSON."}), 400

    mensagens, err = _validar_mensagens(data)
    if err:
        return jsonify({"error": err}), 422

    try:
        dialogo, analise = criar_e_analisar(mensagens)
        return jsonify({
            "id": dialogo.id,
            "status": "analisado",
            "score": analise.score_final,
        }), 201
    except Exception as e:
        from flask import current_app
        current_app.logger.exception("Erro ao criar diálogo")
        return jsonify({"error": "Erro ao processar o diálogo."}), 500


@bp.route("/dialogos", methods=["GET"])
def get_dialogos():
    """Lista diálogos com paginação."""
    limit = min(int(request.args.get("limit", 50)), 100)
    offset = max(int(request.args.get("offset", 0)), 0)
    dialogos = listar_dialogos(limit=limit, offset=offset)
    items = []
    for d in dialogos:
        analise = d.analises.order_by(Analise.data_calculo.desc()).first() if d.analises else None
        score = analise.score_final if analise else None
        items.append({
            "id": d.id,
            "data_criacao": d.data_criacao.isoformat() if d.data_criacao else None,
            "quantidade_mensagens": d.mensagens.count(),
            "score": score,
        })
    return jsonify({"dialogos": items, "limit": limit, "offset": offset})


@bp.route("/dialogos/<int:dialogo_id>", methods=["GET"])
def get_dialogo(dialogo_id):
    """Detalhes do diálogo (mensagens)."""
    dialogo = obter_dialogo_por_id(dialogo_id)
    if not dialogo:
        return jsonify({"error": "Diálogo não encontrado."}), 404
    mensagens = [
        {
            "id": m.id,
            "autor": m.autor,
            "texto": m.texto,
            "timestamp": m.timestamp.isoformat() if m.timestamp else None,
        }
        for m in dialogo.mensagens.order_by(Mensagem.timestamp)
    ]
    return jsonify({
        "id": dialogo.id,
        "data_criacao": dialogo.data_criacao.isoformat() if dialogo.data_criacao else None,
        "mensagens": mensagens,
    })


@bp.route("/dialogos/<int:dialogo_id>/score", methods=["GET"])
def get_score(dialogo_id):
    """Score, métricas e explicabilidade do diálogo."""
    resultado = obter_score_e_metricas(dialogo_id)
    if not resultado:
        return jsonify({"error": "Diálogo ou análise não encontrada."}), 404
    return jsonify(resultado)
