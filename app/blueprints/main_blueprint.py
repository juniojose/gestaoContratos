from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from app.models import Menu, UsuariosPreferencias, MiniApp
from app import db
from flask_login import login_required, current_user
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

main_bp = Blueprint('main_bp', __name__)

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
        # Registrar log de acesso à aplicação
        registrar_log(miniAppId=None, logAcao="Acesso à Aplicação", logResultadoAcao=True)

        # Redireciona para a página home
        return redirect(url_for('main_bp.home'))
    else:
        # Registrar log de tentativa de acesso não autenticado
        registrar_log(miniAppId=None, logAcao="Tentativa de Acesso Não Autenticado", logResultadoAcao=False)

        # Redireciona para a página de login
        return redirect(url_for('auth.login'))

# Rota para a página inicial
@main_bp.route("/home")
@login_required
def home():
    # Recuperar o registro de preferências do usuário logado
    preferencias = UsuariosPreferencias.query.filter_by(usuarioId=current_user.usuarioId).first()

    # Obter os MiniApps selecionados pelo usuário para exibição na Home
    miniapps_home = []
    if preferencias and preferencias.preferenciaMiniAppsHome:
        miniapps_home_ids = preferencias.preferenciaMiniAppsHome
        miniapps_home = MiniApp.query.filter(MiniApp.miniAppId.in_(miniapps_home_ids)).all()

    # Renderizar a Home com os MiniApps selecionados
    return render_template('home.html', miniapps=miniapps_home)

@main_bp.route('/extend_session', methods=['POST'])
@login_required
def extend_session():
    session.modified = True  # Atualiza a sessão para estender o tempo de validade

    # Registrar log de extensão da sessão
    registrar_log(miniAppId=None, logAcao="Extensão de Sessão", logResultadoAcao=True)

    return '', 204  # Retorna resposta sem conteúdo
