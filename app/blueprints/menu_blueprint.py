from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app.forms import MenuForm
from app.models import Menu, MiniApp
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from flask_login import current_user

menu_bp = Blueprint('menus', __name__, template_folder='templates')

# Lista os menus
@menu_bp.route("/", methods=["GET"])
@login_required
def list_menus():
    page = request.args.get("page", 1, type=int)
    menus = Menu.query.order_by(Menu.menuOrdem).paginate(page=page, per_page=10, error_out=False)
    return render_template("list_menus.html", menus=menus.items, pagination=menus)

# Cria um novo menu
@menu_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_menu():
    form = MenuForm()
    if form.validate_on_submit():
        menu = Menu(
            menuNome=form.menuNome.data,
            menuOrdem=form.menuOrdem.data,
            menuTemplate=form.menuTemplate.data,
        )
        db.session.add(menu)
        try:
            db.session.commit()
            flash("Menu criado com sucesso!", "success")
            return redirect(url_for("menus.list_menus"))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um menu com esse nome ou template.", "danger")
    return render_template("menu_form.html", form=form, title="Novo Menu")

# Edita um menu existente
@menu_bp.route("/edit/<int:menu_id>", methods=["GET", "POST"])
@login_required
def edit_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    form = MenuForm(obj=menu)

    if form.validate_on_submit():
        # Verifica se já existe outro menu com o mesmo nome
        existing_menu = Menu.query.filter(Menu.menuNome == form.menuNome.data, Menu.menuId != menu_id).first()
        if existing_menu:
            flash("Erro: Já existe um menu com esse nome.", "danger")
            return render_template("menu_form.html", form=form, title="Editar Menu")

        # Verifica se já existe outro template com o mesmo nome
        existing_template = Menu.query.filter(Menu.menuTemplate == form.menuTemplate.data, Menu.menuId != menu_id).first()
        if existing_template:
            flash("Erro: Já existe um menu com esse template.", "danger")
            return render_template("menu_form.html", form=form, title="Editar Menu")

        # Atualiza os campos do menu
        menu.menuNome = form.menuNome.data
        menu.menuOrdem = form.menuOrdem.data
        menu.menuTemplate = form.menuTemplate.data

        try:
            db.session.commit()  # Salva as alterações no banco de dados
            flash("Menu atualizado com sucesso!", "success")
            return redirect(url_for("menus.list_menus"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar o menu: {str(e)}", "danger")

    return render_template("menu_form.html", form=form, title="Editar Menu")

# Deleta um menu
@menu_bp.route("/delete/<int:menu_id>", methods=["POST"])
@login_required
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    flash("Menu excluído com sucesso!", "success")
    return redirect(url_for("menus.list_menus"))

from app.models import MiniApp, PerfisPermissoes, UsuariosPermissoes

@menu_bp.route("/<menu_template>", methods=["GET"])
@login_required
def dynamic_menu(menu_template):
    menu = Menu.query.filter_by(menuTemplate=menu_template).first_or_404()

    # Recuperar todos os MiniApps do menu
    all_mini_apps = MiniApp.query.filter_by(menuId=menu.menuId).all()

    # Filtrar MiniApps com base nas permissões do usuário
    allowed_mini_apps = []
    for mini_app in all_mini_apps:
        # Verifica se o MiniApp está nas permissões do perfil do usuário
        perfil_permissao = any(
            permissao.miniAppId == mini_app.miniAppId
            for permissao in current_user.perfil.perfisPermissoes
        )

        # Verifica se o MiniApp está nas permissões diretas do usuário
        usuario_permissao = any(
            permissao.miniAppId == mini_app.miniAppId
            for permissao in current_user.usuariosPermissoes
        )

        # Adiciona o MiniApp se o usuário tem permissão
        if perfil_permissao or usuario_permissao:
            allowed_mini_apps.append(mini_app)

    return render_template("default_menu.html", menu=menu, mini_apps=allowed_mini_apps)