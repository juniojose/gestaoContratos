from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import MenuForm
from app.models import Menu
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

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
        )
        db.session.add(menu)
        try:
            db.session.commit()
            flash("Menu criado com sucesso!", "success")
            return redirect(url_for("menus.list_menus"))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um menu com esse nome.", "danger")
    return render_template("menu_form.html", form=form, title="Novo Menu")

# Edita um menu existente
@menu_bp.route("/edit/<int:menu_id>", methods=["GET", "POST"])
@login_required
def edit_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    form = MenuForm(obj=menu, menuId=menu.menuId)  # Passa o menuId ao formulário

    if form.validate_on_submit():
        # Atualiza os campos do menu
        menu.menuNome = form.menuNome.data
        menu.menuOrdem = form.menuOrdem.data

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
