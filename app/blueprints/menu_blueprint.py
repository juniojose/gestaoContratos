from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import MenuForm
from app.models import Menu
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.middlewares import permission_required

menu_bp = Blueprint('menu', __name__, template_folder='templates')

# Lista os menus com paginação
@menu_bp.route("/", methods=['GET'])
@login_required
@permission_required(miniAppId=2)
def list_menu():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Define o número de itens por página
    pagination = Menu.query.order_by(Menu.menuNome).paginate(page=page, per_page=per_page)
    return render_template('list_menu.html', menus=pagination.items, pagination=pagination)

# Cria um novo menu
@menu_bp.route("/new", methods=['GET', 'POST'])
@login_required
def new_menu():
    form = MenuForm()
    if form.validate_on_submit():
        menu = Menu(menuNome=form.menuNome.data)
        db.session.add(menu)
        try:
            db.session.commit()
            flash("Menu cadastrado com sucesso!", "success")
            return redirect(url_for('menu.list_menu'))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um menu com esse nome.", "error")
    return render_template('menu_form.html', form=form, title='Cadastro de Menu')

# Edita um menu existente
@menu_bp.route("/edit/<int:menu_id>", methods=['GET', 'POST'])
@login_required
def edit_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    form = MenuForm()
    if form.validate_on_submit():
        menu.menuNome = form.menuNome.data
        try:
            db.session.commit()
            flash("Menu atualizado com sucesso!", "success")
            return redirect(url_for('menu.list_menu'))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um menu com esse nome.", "error")
    elif request.method == 'GET':
        form.menuNome.data = menu.menuNome
    return render_template('menu_form.html', form=form, title='Editar Menu')

# Deleta um menu
@menu_bp.route("/delete/<int:menu_id>", methods=['POST'])
@login_required
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    try:
        db.session.delete(menu)
        db.session.commit()
        flash("Menu deletado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao deletar menu: {str(e)}", "error")
    return redirect(url_for('menu.list_menu'))
