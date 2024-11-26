import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa extensões
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app():
    # Cria a aplicação Flask
    app = Flask(__name__)

    # Configura a aplicação
    configure_app(app)

    # Inicializa extensões com a aplicação
    initialize_extensions(app)

    # Registra blueprints
    register_blueprints(app)

    return app

def configure_app(app):
    """Configura a aplicação com variáveis de ambiente."""
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dados.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def initialize_extensions(app):
    """Inicializa as extensões com a aplicação."""
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    """Registra os blueprints com a aplicação."""
    from .blueprints.status_blueprint import status_bp
    app.register_blueprint(status_bp, url_prefix='/status')  # Prefixo /status

    from .blueprints.fazendas_blueprint import fazendas_bp
    app.register_blueprint(fazendas_bp, url_prefix='/fazendas')  # Prefixo /fazenda

    from .blueprints.usuariosperfis_blueprint import usuariosperfis_bp
    app.register_blueprint(usuariosperfis_bp, url_prefix='/usuariosperfis')  # Prefixo /usuariosperfis

    # Importe e registre o blueprint main_bp
    from .blueprints.main_blueprint import main_bp
    app.register_blueprint(main_bp, url_prefix='/')  # Sem prefixo para as rotas principais
