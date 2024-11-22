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

class UsuariosPerfis(db.Model):  # Certifique-se de que o nome está correto
    __tablename__ = 'usuariosPerfis'

    perfilId = db.Column(db.Integer, primary_key=True)
    statusId = db.Column(db.Integer, db.ForeignKey('status.statusId'), nullable=False)
    perfilNome = db.Column(db.String(50), unique=True, nullable=False)
    perfilDescricao = db.Column(db.String(100), nullable=True)
    perfilDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    perfilDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com Status
    status = db.relationship('Status', backref=db.backref('usuariosPerfis', lazy=True))

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuarioId = db.Column(db.Integer, primary_key=True)
    statusId = db.Column(db.Integer, db.ForeignKey('status.statusId'), nullable=False)
    fazendaId = db.Column(db.Integer, db.ForeignKey('fazendas.fazendaId'), nullable=True)
    usuarioPerfilId = db.Column(db.Integer, db.ForeignKey('usuariosPerfis.perfilId'), nullable=False)
    usuarioNome = db.Column(db.String(150), nullable=False)
    usuarioEmail = db.Column(db.String(255), unique=True, nullable=False)
    usuarioSenha = db.Column(db.String(255), nullable=False)
    usuarioDataValidadePermissao = db.Column(db.DateTime, nullable=True)
    usuarioDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    usuarioDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    status = db.relationship('Status', backref=db.backref('usuarios', lazy=True))
    fazenda = db.relationship('Fazenda', backref=db.backref('usuarios', lazy=True))
    perfil = db.relationship('UsuariosPerfis', backref=db.backref('usuarios', lazy=True))
