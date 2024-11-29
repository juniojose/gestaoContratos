from . import db
from datetime import datetime
from flask_login import UserMixin

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

class UsuariosPerfis(db.Model):
    __tablename__ = 'usuariosPerfis'

    perfilId = db.Column(db.Integer, primary_key=True)
    statusId = db.Column(db.Integer, db.ForeignKey('status.statusId'), nullable=False)
    perfilNome = db.Column(db.String(50), unique=True, nullable=False)
    perfilDescricao = db.Column(db.String(100), nullable=True)
    perfilDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    perfilDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com Status
    status = db.relationship('Status', backref=db.backref('usuariosPerfis', lazy=True))

class Usuario(db.Model, UserMixin):
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

    def get_id(self):
        return str(self.usuarioId)

class Menu(db.Model):
    __tablename__ = 'menus'

    menuId = db.Column(db.Integer, primary_key=True)
    menuNome = db.Column(db.String(30), unique=True, nullable=False)
    menuOrdem = db.Column(db.Integer, nullable=False)
    menuTemplate = db.Column(db.String(50), unique=True, nullable=False)
    menuDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    menuDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MiniApp(db.Model):
    __tablename__ = 'miniApps'

    miniAppId = db.Column(db.Integer, primary_key=True)
    miniAppNome = db.Column(db.String(100), unique=True, nullable=False)
    miniAppIcon = db.Column(db.String(40), nullable=False)
    miniAppLink = db.Column(db.String(200), nullable=True)  # Temporariamente nullable
    menuId = db.Column(db.Integer, db.ForeignKey('menus.menuId'), nullable=False)
    miniAppDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    miniAppDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com Menu
    menu = db.relationship('Menu', backref=db.backref('miniApps', lazy=True))

class PerfisPermissoes(db.Model):
    __tablename__ = 'perfisPermissoes'

    perfilPermissaoId = db.Column(db.Integer, primary_key=True)
    perfilId = db.Column(db.Integer, db.ForeignKey('usuariosPerfis.perfilId'), nullable=False)
    miniAppId = db.Column(db.Integer, db.ForeignKey('miniApps.miniAppId'), nullable=False)
    perfilPermissaoDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    perfilPermissaoDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    perfil = db.relationship('UsuariosPerfis', backref=db.backref('perfisPermissoes', lazy=True))
    miniApp = db.relationship('MiniApp', backref=db.backref('perfisPermissoes', lazy=True))

class UsuariosPermissoes(db.Model):
    __tablename__ = 'usuariosPermissoes'

    permissaoId = db.Column(db.Integer, primary_key=True)
    statusId = db.Column(db.Integer, db.ForeignKey('status.statusId'), nullable=False)
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioId'), nullable=False)
    miniAppId = db.Column(db.Integer, db.ForeignKey('miniApps.miniAppId'), nullable=False)
    permissaoMotivo = db.Column(db.String(255), nullable=True)
    permissaoDataCadastro = db.Column(db.DateTime, default=datetime.utcnow)
    permissaoDataUltimaAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    status = db.relationship('Status', backref=db.backref('usuariosPermissoes', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('usuariosPermissoes', lazy=True))
    miniApp = db.relationship('MiniApp', backref=db.backref('usuariosPermissoes', lazy=True))
