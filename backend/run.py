import os
from app import create_app
from app.extensions import socketio

# Mudar para production quando for colocar em produção
app = create_app(config_name=os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=app.config.get("DEBUG", True),
        use_reloader=app.config.get("DEBUG", True),
        allow_unsafe_werkzeug=True, # TODO: remover quando for pra PROD
    )
