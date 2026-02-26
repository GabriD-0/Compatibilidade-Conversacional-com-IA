from datetime import datetime
from time import timezone
from app import db

# TODO: Reavaliar colunas

"""Modelos Analise (score) e Metricas."""
class Analise(db.Model):
    __tablename__ = "analises"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    dialogo_id = db.Column(db.Integer, db.ForeignKey("dialogos.id"), nullable=False)
    score_final = db.Column(db.Float, nullable=False)
    data_calculo = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    versao = db.Column(db.Integer, default=1)
    metricas = db.relationship("Metricas", backref="analise", uselist=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Metricas(db.Model):
    __tablename__ = "metricas"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    analise_id = db.Column(db.Integer, db.ForeignKey("analises.id"), nullable=False)
    lsm = db.Column(db.Float, nullable=True)
    metricas_sentimento = db.Column(db.JSON, nullable=True)
    metricas_comportamentais = db.Column(db.JSON, nullable=True)
    explicabilidade = db.Column(db.JSON, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))