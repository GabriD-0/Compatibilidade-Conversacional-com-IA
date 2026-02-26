from flask import Blueprint, jsonify
from app import db
from app.models import Dialogo

# TODO: Reavaliar exclusão de dados

bp = Blueprint("dados", __name__)

@bp.route("/dados/<identificador>", methods=["DELETE"])
def excluir_dados(identificador):
    """Exclui dados associados ao identificador (ex.: diálogo por id). LGPD Art. 18."""
    try:
        dialogo_id = int(identificador)
    except ValueError:
        return jsonify({"error": "Identificador inválido."}), 400

    dialogo = db.session.get(Dialogo, dialogo_id)
    if not dialogo:
        return jsonify({"message": "Nenhum dado encontrado para o identificador."}), 200

    # Remover em ordem: Metricas -> Analise -> Mensagem -> Dialogo (ou usar cascade)
    from app.models import Mensagem, Analise, Metricas
    for analise in dialogo.analises:
        if analise.metricas:
            db.session.delete(analise.metricas)
        db.session.delete(analise)
    for msg in dialogo.mensagens:
        db.session.delete(msg)
    db.session.delete(dialogo)
    db.session.commit()
    return jsonify({"message": "Dados excluídos com sucesso."}), 200
