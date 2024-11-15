from . import db
from datetime import datetime

class Status(db.Model):
    __tablename__ = 'status'

    statusId = db.Column(db.Integer, primary_key=True)
    statusDescricao = db.Column(db.String(100), unique=True, nullable=False)
    statusDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    statusDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fazenda(db.Model):
    __tablename__ = 'fazendas'

    fazendaId = db.Column(db.Integer, primary_key=True)
    statusId = db.Column(db.Integer, db.ForeignKey('status.statusId'), nullable=False)
    fazendaSigla = db.Column(db.String(2), unique=True, nullable=False)
    fazendaNome = db.Column(db.String(50), unique=True, nullable=False)
    fazendaCEP = db.Column(db.String(8), nullable=False)
    fazendaEstado = db.Column(db.String(50), nullable=False)
    fazendaCidade = db.Column(db.String(50), nullable=False)
    fazendaBairro = db.Column(db.String(100), nullable=True)
    fazendaLogradouro = db.Column(db.String(100), nullable=True)
    fazendaNumero = db.Column(db.String(6), nullable=True)
    fazendaComplemento = db.Column(db.String(50), nullable=True)
    fazendaDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    fazendaDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com Status
    status = db.relationship('Status', backref=db.backref('fazendas', lazy=True))