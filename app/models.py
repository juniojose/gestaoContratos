from . import db
from datetime import datetime

class Status(db.Model):
    __tablename__ = 'status'

    statusId = db.Column(db.Integer, primary_key=True)
    statusDescricao = db.Column(db.String(100), unique=True, nullable=False)
    statusDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    statusDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
