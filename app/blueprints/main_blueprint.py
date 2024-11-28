from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import StatusForm, FazendaForm, UsuariosPerfisForm
from app.models import Status, Fazenda, UsuariosPerfis, Menu, PerfisPermissoes
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from flask_login import current_user
from flask import Blueprint, render_template, session, redirect, url_for, flash, g

main_bp = Blueprint('main_bp', __name__)

from app.models import Menu

@main_bp.before_app_request
def load_menus():
    if current_user.is_authenticated:
        menus = Menu.query.order_by(Menu.menuOrdem).all()  # Ordena pela ordem definida
        g.menus = menus
    else:
        g.menus = []

# Rota para login
@main_bp.route("/", methods=['GET', 'POST'])
def index():
    # Verifica se o usuário está autenticado
    if current_user.is_authenticated:
        # Redireciona para a página home
        return redirect(url_for('main_bp.home'))
    else:
        # Redireciona para a página de login
        return redirect(url_for('auth.login'))


# Rota para a página inicial
@main_bp.route("/home")
@login_required
def home():
    # Recuperar um menu específico
    menu = Menu.query.filter_by(menuTemplate='home').first()

    # Certifique-se de que o menu foi encontrado
    if not menu:
        return "Menu não encontrado", 404

    # Renderizar o template com a variável `menu`
    return render_template('home.html', menu=menu)

@main_bp.route('/extend_session', methods=['POST'])
@login_required
def extend_session():
    session.modified = True  # Atualiza a sessão para estender o tempo de validade
    return '', 204  # Retorna resposta sem conteúdo

