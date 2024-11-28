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
@login_required
def login():
    return redirect(url_for('main_bp.home'))

# Rota para a página inicial
@main_bp.route("/home")
@login_required
def home():
    return render_template('home.html')

@main_bp.route('/extend_session', methods=['POST'])
@login_required
def extend_session():
    session.modified = True  # Atualiza a sessão para estender o tempo de validade
    return '', 204  # Retorna resposta sem conteúdo

