import logging
from flask import jsonify, request

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        logger.warning("Bad request: %s", request.path)
        return jsonify({"error": "Requisição inválida", "detail": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": "Dados inválidos", "detail": str(e)}), 422

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Internal server error")
        return jsonify({"error": "Erro interno do servidor"}), 500
