from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from app.models import Menu
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
    # Recuperar um menu específico
    menu = Menu.query.filter_by(menuTemplate='home').first()

    # Certifique-se de que o menu foi encontrado
    if not menu:
        # Registrar log de falha ao acessar a página inicial
        registrar_log(miniAppId=None, logAcao="Acesso à Página Inicial", logResultadoAcao=False)
        return "Menu não encontrado", 404

    # Registrar log de sucesso ao acessar a página inicial
    registrar_log(miniAppId=None, logAcao="Acesso à Página Inicial", logResultadoAcao=True)

    # Renderizar o template com a variável `menu`
    return render_template('home.html', menu=menu)

@main_bp.route('/extend_session', methods=['POST'])
@login_required
def extend_session():
    session.modified = True  # Atualiza a sessão para estender o tempo de validade

    # Registrar log de extensão da sessão
    registrar_log(miniAppId=None, logAcao="Extensão de Sessão", logResultadoAcao=True)

    return '', 204  # Retorna resposta sem conteúdo
