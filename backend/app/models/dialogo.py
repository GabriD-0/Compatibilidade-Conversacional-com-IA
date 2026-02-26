from datetime import datetime
from time import timezone
from app import db

# TODO: Reavaliar colunas

class Dialogo(db.Model):
    __tablename__ = "dialogos"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    identificador_externo = db.Column(db.String(64), unique=True, nullable=True, index=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    versao_calculo = db.Column(db.Integer, default=1)
    mensagens = db.relationship("Mensagem", backref="dialogo", lazy="dynamic", order_by="Mensagem.timestamp")
    analises = db.relationship("Analise", backref="dialogo", lazy="dynamic")
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Mensagem(db.Model):
    __tablename__ = "mensagens"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    dialogo_id = db.Column(db.Integer, db.ForeignKey("dialogos.id"), nullable=False)
    autor = db.Column(db.String(64), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))