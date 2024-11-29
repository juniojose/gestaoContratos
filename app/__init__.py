import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask import render_template
from dotenv import load_dotenv
from datetime import timedelta

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa extensões
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    # Cria a aplicação Flask
    app = Flask(__name__)

    # Configura a aplicação
    configure_app(app)

    # Inicializa extensões com a aplicação
    initialize_extensions(app)

    # Registra blueprints
    register_blueprints(app)

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

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
    login_manager.init_app(app)  # Inicializa o gerenciador de login
    login_manager.login_view = "auth.login"  # Define a rota de login
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"
    app.permanent_session_lifetime = timedelta(minutes=10)  # Sessão expira após 10 minutos

    # Função para carregar o usuário pelo ID
    from app.models import Usuario  # Importa o modelo Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

def register_blueprints(app):
    """Registra os blueprints com a aplicação."""
    from .blueprints.status_blueprint import status_bp
    app.register_blueprint(status_bp, url_prefix='/status')

    from .blueprints.fazendas_blueprint import fazendas_bp
    app.register_blueprint(fazendas_bp, url_prefix='/fazendas')

    from .blueprints.usuariosperfis_blueprint import usuariosperfis_bp
    app.register_blueprint(usuariosperfis_bp, url_prefix='/usuariosperfis')

    # Importe e registre o blueprint main_bp
    from .blueprints.main_blueprint import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    # Importe e registre o blueprint usuarios_bp
    from .blueprints.usuarios_blueprint import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    from .blueprints.menu_blueprint import menu_bp
    app.register_blueprint(menu_bp, url_prefix='/menus')

    from .blueprints.miniapp_blueprint import miniapps_bp
    app.register_blueprint(miniapps_bp, url_prefix='/miniapps')

    from .blueprints.perfispermissoes_blueprint import perfispermissoes_bp
    app.register_blueprint(perfispermissoes_bp, url_prefix='/perfisPermissoes')

    from .blueprints.auth_blueprint import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .blueprints.usuariospermissoes_blueprint import usuariospermissoes_bp
    app.register_blueprint(usuariospermissoes_bp, url_prefix='/usuariospermissoes')
